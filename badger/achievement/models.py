#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from repository.models import Contributor


class ContributorAchievement(models.Model):
    achievement = models.CharField(max_length=100, db_index=True)
    contributor = models.ForeignKey(Contributor)

