#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

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
    BADGES_CLASSES = []
    BADGES_CLASSES.append(CommitCount)
    for badge_class_name in getattr(settings, 'BADGES_ENABLED', []):
        try:
            BADGES_CLASSES.append(import_class(badge_class_name))
        except Exception, e:
            logging.info(u"Coun't import badge class (%s) the error was: %s" % (badge_class_name, str(e)))
    return BADGES_CLASSES


class Badge(object):
    slug = 'default_badge'
    description = 'default_description'

    def __init__(self, user_email):
        self.user_email = user_email

    def process_commit(self, commit, commit_date):
        pass

    def award_this(self):
        raise NotImplementedError


class NewbieBadge(Badge):
    slug = 'newbie-badger'

    def process_commit(self, commit, commit_date):
        if commit.author.email == self.user_email:
            self.has_this_badge = True

    def award_this(self):
        return self.has_this_badge

class BigNiceBadge(Badge):
    slug = 'big-nice-badger'

    def __init__(self, *args, **kw):
        super(BigNiceBadge, self).__init__(*args, **kw)
        self.count = 0

    def process_commit(self, commit, commit_date):
        if commit.author.email == self.user_email:
            self.count += 1

    def award_this(self):
        return self.count >= 30

class AlmostBadBadge(Badge):
    slug = 'almost-bad-badger'

    def __init__(self, *args, **kw):
        super(AlmostBadBadge, self).__init__(*args, **kw)
        self.count = 0

    def process_commit(self, commit, commit_date):
        if commit.author.email == self.user_email:
            self.count += 1

    def award_this(self):
        return self.count >= 50


class BigBadBadge(Badge):
    slug = 'big-bad-badger'

    def __init__(self, *args, **kw):
        super(BigBadBadge, self).__init__(*args, **kw)
        self.count = 0

    def process_commit(self, commit, commit_date):
        if commit.author.email == self.user_email:
            self.count += 1

    def award_this(self):
        return self.count >= 100

class BadgerKahuna(Badge):
    slug = 'badger-kahuna'

    def __init__(self, *args, **kw):
        super(BadgerKahuna, self).__init__(*args, **kw)
        self.count = 0

    def process_commit(self, commit, commit_date):
        if commit.author.email == self.user_email:
            self.count += 1

    def award_this(self):
        return self.count >= 300


class CommitCount:

    def __init__(self, email, *args, **kw):
        self.user_email = email
        self.count = 0

    def process_commit(self, commit, commit_date):
        if commit.author.email == self.user_email:
            self.count += 1

    def update_data(self):
        return {'total_commits': self.count}



