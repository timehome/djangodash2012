#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Repository(models.Model):
    name = models.CharField(max_length=100)
    homepage = models.URLField()
    git_url = models.CharField(max_length=200)

class UnknownUser(models.Model):
    email = models.CharField(max_length=200)

class Contributor(models.Model):
    repository = models.ForeignKey(Repository)
    contributor = models.ForeignKey(User, null=True, blank=True)
    unknown_contributor = models.ForeignKey(UnknownUser, null=True, blank=True)