#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging

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

    def process_commit(self, commit, lines_added, lines_removed):
        pass

    def process_repositories(self, repositories):
        pass

    def award_this(self):
        raise NotImplementedError


class NewbieBadge(Badge):
    slug = 'newbie_badge'

    def process_commit(self, commit, lines_added, lines_removed):
        if commit.author.email == self.user_email:
            self.has_this_badge = True

    def award_this(self):
        return self.has_this_badge


class RepositoryProcessor(object):

    def __init__(self, repository_path):
        self.repository_path = repository_path

    def process(self):
        # returns the json of the collaborators
        pass


class RepositoryWorker(object):

    @classmethod
    def perform(cls, repository, token, email):
        import ipdb;ipdb.set_trace()
        
        all_match, username, repo_name = re.match('github.com/([\w_]+)/([\w_]+)', repository.url).groups()
        gh = Github(user=username, token=token)
        repository = gh.repos.get(user=username, repo=repository_name)

