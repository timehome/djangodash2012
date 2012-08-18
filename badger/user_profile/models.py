import hashlib
from django.db import models
from django.contrib.auth.models import User
from social_auth.fields import JSONField

class BadgerProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    extra_data = JSONField(default='{}')

    def thumb_url(self, size=80):
        email_md5 = hashlib.md5(self.extra_data['email'].lower()).hexdigest()
        return 'http://www.gravatar.com/avatar/%s?s=%s' % (email_md5, size)

