#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from repository.models import Contributor


class ContributorAchievement(models.Model):
    BADGE_DESCRIPTION = {'newbie-badger': 'this badger is no stranger to git (1 commit in this project)',
                         'big-nice-badger': "You're almost there. Keep up the good work! (30+ commits in this project)",
                         'almost-bad-badger': "Wow! Do that again and wait for rainbows and unicorns. (50+ commits in this project)",
                         'big-bad-badger': "who's afraid of this big bad badger? (100+ commits in this project)",
                         'badger-kahuna': "Looks like we have a big kahuna among us! (300+ commits in this project)"}

    achievement = models.CharField(max_length=100, db_index=True)
    contributor = models.ForeignKey(Contributor)

    def description(self):
      return self.BADGE_DESCRIPTION[self.achievement]


