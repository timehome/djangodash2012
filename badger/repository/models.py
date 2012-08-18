#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Repository(models.Model):
    name = models.CharField(max_length=100)
    homepage = models.UrlField()
    git_url = models.CharField(max_length=200)

class UnknownUser(models.Model):
    email = models.CharField(max_length=200)
    real_user = models.ForeignKey(User, null=True, empty=True)

class ProcessedUsers(models.Model):
    unknown_user = models.ForeignKey(UnknownUser)
    repository = models.ForeignKey(Repository, related_name='processed_users')
