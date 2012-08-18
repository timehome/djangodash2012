#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Repository(models.Model):
    name = models.CharField(max_length=100)
    git_url = models.CharField(max_length=200, db_index=True)
    html_url = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)

class UnknownUser(models.Model):
    email = models.CharField(max_length=200, db_index=True)

class Contributor(models.Model):
    repository = models.ForeignKey(Repository)
    user = models.ForeignKey(User, null=True, blank=True)
    unknown_contributor = models.ForeignKey(UnknownUser, null=True, blank=True)
    addtions = models.IntegerField(default=0, blank=True)
    remotions = models.IntegerField(default=0, blank=True)
    commmits = models.IntegerField(default=0, blank=True)
