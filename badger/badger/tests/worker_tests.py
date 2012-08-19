#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest

from badger.badges.processor import RepositoryWorker, count_modifications_by_user
from repository.models import Repository, UnknownUser, Contributor


class BadgeWorkerTestCase(unittest.TestCase):

    def test_process_of_repository(self):
        user = {
            "email": "rafael.jacinto@gmail.com",
            "token": "abcdef",
            "repo": {
                "name": 'insthumbor',
                "url": "git://github.com/rafaelcaricio/insthumbor.git",
                "git_url": "git://github.com/rafaelcaricio/insthumbor.git",
                "html_url": "git://github.com/rafaelcaricio/insthumbor.git",
                "language": "Python"
            }
        }
        RepositoryWorker.perform(user)

        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(UnknownUser.objects.count(), 3)
        self.assertEqual(Contributor.objects.count(), 3)
        self.assertTrue(Contributor.objects.all()[0].total_commits > 0)

