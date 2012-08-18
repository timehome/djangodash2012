#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


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
    def process_repository(cls, repository_name, repository_url, username, token):
        pass

