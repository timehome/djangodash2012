from django.db import models
from repository.models import Contributor


class Achievement(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

class UserAchievement(models.Model):
    achievement = models.ForeignKey(Achievement)
    contributor = models.ForeignKey(Contributor)


