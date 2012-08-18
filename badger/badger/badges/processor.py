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

from badger.badges import Badge, BADGES_CLASSES


class RepositoryProcessor(object):

    def __init__(self, repository_path):
        self.repo = GitRepository(repository_path + '/.git')
        self.users = {}

    def get_bages_processors_for_user(self, email):
        if email in self.users:
            return self.users[email]
        self.users[email] = []
        for badge_class in BADGES_CLASSES:
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

    @classmethod
    def perform(cls, user):
        temp_dir = None
        try:

            username, repo_name = re.search('github\.com/([\w_]+)/([\w_]+)', user["repo"]["url"]).groups()

            try:
                db_repo = Repository.objects.get(git_url=user['repo']['url'])
            except Repository.DoesNotExist:
                gh = Github() #login=user['email'], token=user['token'])
                repo = gh.repos.get(user=username, repo=repo_name)

                db_repo = Repository(name=repo.name,
                        git_url=repo.git_url,
                        html_url=repo.html_url,
                        url=repo.url,
                        language=repo.language)

                db_repo.save()

            temp_dir = tempfile.mkdtemp()
            processor = RepositoryProcessor(clone_repo(user["repo"]["url"], temp_dir))
            response = processor.process()

            with transaction.commit_on_success():
                for unknown_contributor in response:
                    uku, created = UnknownUser.objects.get_or_create(email=unknown_contributor['email'], defaults={
                        "email": unknown_contributor['email']
                    })

                    db_user = None
                    try:
                        db_user = User.objects.get(email=unknown_contributor['email'])
                    except:
                        pass

                    contributor, created = Contributor.objects.get_or_create(unknown_contributor=uku, defaults={
                        "user": db_user,
                        "unknown_contributor": uku,
                        "repository": db_repo,
                        "added_lines": unknown_contributor['added_lines'],
                        "removed_lines": unknown_contributor['removed_lines'],
                        "total_commits": unknown_contributor['total_commits']
                    })

                    for badge in unknown_contributor['badges']:
                        ContributorAchievement.objects.get_or_create(achievement=badge['badge_slug'],
                            contributor=contributor, defaults = {
                            'achievement': badge['badge_slug'],
                            'contributor': contributor
                        })
        finally:
            if exists(temp_dir):
                shutil.rmtree(temp_dir)

