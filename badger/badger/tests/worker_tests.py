#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from badger.badges import RepositoryWorker, initialize_badge_classes

initialize_badge_classes()

class BadgeWorkerTestCase(unittest.TestCase):

    def test_process_of_repository(self):
        user = {
            "email": "rafael.jacinto@gmail.com",
            "token": "abcdef",
            "repo": {
                "name": 'thumbor',
                "url": "git://github.com/globocom/thumbor.git"
            }
        }
        RepositoryWorker.perform(user)


