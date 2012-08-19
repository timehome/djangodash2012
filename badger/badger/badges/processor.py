#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import json
import logging
import tempfile
import shutil
from os.path import exists
import subprocess
from datetime import datetime

from pygit2 import Repository as GitRepository
from pygit2 import GIT_SORT_TIME
from pygithub3 import Github
from django.db import transaction

from achievement.models import ContributorAchievement
from repository.models import Repository, UnknownUser, Contributor

from badger.badges import Badge, initialize_badge_classes


class RepositoryProcessor(object):

    def __init__(self, repository_path):
        self.repo = GitRepository(repository_path + '/.git')
        self.users = {}

    def get_bages_processors_for_user(self, email):
        if email in self.users:
            return self.users[email]
        self.users[email] = []
        for badge_class in initialize_badge_classes():
            self.users[email].append(badge_class(email))
        return self.users[email]

    def process(self):
        # returns the json of the collaborators
        for commit in [c for c in self.repo.walk(self.repo.head.oid, GIT_SORT_TIME)][::-1]:
            for badge in self.get_bages_processors_for_user(commit.author.email):
                badge.process_commit(commit, datetime.fromtimestamp(commit.commit_time))
        result = []
        for user_email, badges in self.users.items():
            user = {"email": user_email, "badges": []}
            result.append(user)
            for badge in badges:
                if isinstance(badge, Badge):
                    if badge.award_this():
                        user['badges'].append({"badge_slug": badge.slug})
                else:
                    user.update(badge.update_data())
            user.update(count_modifications_by_user(user_email, self.repo.path))
        return result



class CantCloneRepositoryException(Exception):
    pass


def clone_repo(git_repo_url, directory):
    if subprocess.call(['git', 'clone', git_repo_url, directory]):
        raise CantCloneRepositoryException()
    else:
        logging.info('Cloned repository %s into %s ...' % (git_repo_url, directory))
        return directory

def count_modifications_by_user(email, directory):
    directory = directory.replace('.git/', '')
    command = """cd %s && /usr/bin/git log --author="%s" --pretty=tformat: --numstat | awk '{ add += $1 ; subs += $2 ; loc += $1 - $2 } END { printf "{\"added_lines\":%%s,\"removed_lines\":%%s,\"total_lines\":%%s}\n",add,subs,loc }'""" % (directory, email)
    result = {"added_lines":0,"removed_lines":0,"total_lines":0}
    try:
        result = json.loads(subprocess.check_output(command))
    finally:
        return result

class RepositoryWorker(object):

    queue = 'repo_queue'

    @classmethod
    def perform(cls, user):
        temp_dir = ''
        try:
            with transaction.commit_on_success():

                repo = user['repo']

                logging.info(u'Initializing process of analysis of the repository [%s]' % repo['git_url'])

                db_repo, created = Repository.objects.get_or_create(
                        git_url=repo['git_url'],
                        defaults=dict(
                            name=repo['name'],
                            git_url=repo['git_url'],
                            html_url=repo['html_url'],
                            url=repo['url'],
                            language=repo['language']
                        )
                )


                temp_dir = tempfile.mkdtemp()
                processor = RepositoryProcessor(clone_repo(repo["git_url"], temp_dir))
                response = processor.process()

                for unknown_contributor in response:
                    uku, created = UnknownUser.objects.get_or_create(email=unknown_contributor['email'], defaults={
                        "email": unknown_contributor['email']
                    })

                    logging.info(u'Saving contributor [%s] ...' % unknown_contributor['email'])

                    db_user = None
                    query_filter = {'unknown_contributor': uku, 'repository': db_repo}
                    try:
                        db_user = User.objects.get(email=unknown_contributor['email'])
                        query_filter = {'user': db_use, 'repository': db_repo}
                    except:
                        pass

                    query_filter.update({'defaults': {
                            "user": db_user,
                            "unknown_contributor": uku,
                            "repository": db_repo,
                            "added_lines": unknown_contributor.get('added_lines', 0),
                            "removed_lines": unknown_contributor.get('removed_lines', 0),
                            "total_commits": unknown_contributor.get('total_commits', 0)
                        }
                    })

                    contributor, created = Contributor.objects.get_or_create(**query_filter)

                    if not created and not contributor.unknown_contributor:
                        contributor.unknown_contributor = uku
                        contributor.save()

                    for badge in unknown_contributor['badges']:
                        ContributorAchievement.objects.get_or_create(achievement=badge['badge_slug'],
                            contributor=contributor, defaults = {
                            'achievement': badge['badge_slug'],
                            'contributor': contributor
                        })
                        logging.info('Contributor [%s] has badge [%s]' % (unknown_contributor['email'], badge['badge_slug']))
        finally:
            if exists(temp_dir):
                shutil.rmtree(temp_dir)

