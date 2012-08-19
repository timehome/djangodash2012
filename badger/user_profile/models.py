import hashlib
from django.db import models
from django.contrib.auth.models import User
from social_auth.fields import JSONField

class BadgerProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    slug = models.SlugField()

    extra_data = JSONField(default='{}')

    @property
    def name(self):
      return self.extra_data['name'].split(' ')[0].lower()

    def thumb_url(self, size=80):
        email_md5 = hashlib.md5(self.extra_data['email'].lower()).hexdigest()
        return 'http://www.gravatar.com/avatar/%s?s=%s' % (email_md5, size)

    @property
    def thumb_url_200_pixels(self):
        return self.thumb_url(200)


