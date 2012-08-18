#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from badger.badges import initialize_badge_classes
from badger.badges.processor import RepositoryWorker
from repository.models import Repository, UnknownUser, Contributor

initialize_badge_classes()

class BadgeWorkerTestCase(unittest.TestCase):

    def test_process_of_repository(self):
        user = {
            "email": "rafael.jacinto@gmail.com",
            "token": "abcdef",
            "repo": {
                "name": 'insthumbor',
                "url": "git://github.com/rafaelcaricio/insthumbor.git"
            }
        }
        RepositoryWorker.perform(user)

        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(UnknownUser.objects.count(), 3)
        self.assertEqual(Contributor.objects.count(), 3)


