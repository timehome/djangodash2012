#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import tempfile

from pygithub3 import Github


BADGES_CLASSES = []


def import_class(name):
    module_name = '.'.join(name.split('.')[:-1])
    klass_name = name.split('.')[-1]
    module = __import__(module_name)
    if '.' in module_name:
        module = reduce(getattr, module_name.split('.')[1:], module)
    return getattr(module, klass_name)


def initialize_badge_classes():
    from django.conf import settings
    for badge_class_name in getattr(settings, 'BADGES_ENABLED', []):
        try:
            BADGES_CLASSES.append(import_class(badge_class_name))
        except Exception, e:
            logging.info(u"Coun't import badge class (%s) the error was: %s" % (badge_class_name, str(e)))


class Badge(object):
    slug = 'default_badge'

    def __init__(self, user_email):
        self.user_email = user_email

    def process_commit(self, commit, commit_date):
        pass

    def award_this(self):
        raise NotImplementedError


class NewbieBadge(Badge):
    slug = 'newbie_badge'

    def process_commit(self, commit, commit_date):
        if commit.author.email == self.user_email:
            self.has_this_badge = True

    def award_this(self):
        return self.has_this_badge


class BigBadBadge(Badge):
    slug = 'bigbad_badge'

    def __init__(self, *args, **kw):
        super(BigBadBadge, self).__init__(*args, **kw)
        self.count = 0

    def process_commit(self, commit, commit_date):
        if commit.author.email == self.user_email:
            self.count += 1

    def award_this(self):
        return self.count >= 100


from datetime import datetime
from pygit2 import Repository
from pygit2 import GIT_SORT_TIME


class RepositoryProcessor(object):

    def __init__(self, repository_path):
        self.repo = Repository(repository_path + '/.git')
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
                if badge.award_this():
                    user['badges'].append({"badge_slug": badge.slug})
            user.update(count_modifications_by_user(user_email, self.repo.path))
        return result


import json
from os import remove
from os.path import exists
import subprocess


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
    command = """cd %s && git log --author="%s" --pretty=tformat: --numstat | awk '{ add += $1 ; subs += $2 ; loc += $1 - $2 } END { printf "{\"added_lines\":%%s,\"removed_lines\":%%s,\"total_lines\":%%s}\n",add,subs,loc }'""" % (directory, email)
    result = {"added_lines":0,"removed_lines":0,"total_lines":0}
    try:
        result = json.loads(subprocess.check_output(command))
    finally:
        return result


class RepositoryWorker(object):

    @classmethod
    def perform(cls, user):
        temp_dir = None
        #try:
        username, repo_name = re.search('github\.com/([\w_]+)/([\w_]+)', user["repo"]["url"]).groups()
        #gh = Github(login=user['email'], token=user['token'])
        #repo = gh.repos.get(user=username, repo=repo_name)

        temp_dir = tempfile.mkdtemp()
        processor = RepositoryProcessor(clone_repo(user["repo"]["url"], temp_dir))
        print processor.process()

        #except Exception, e:
            #print e

