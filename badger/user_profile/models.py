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

    def all_repos(self):
        return self.user.contributor_set.annotate(achievements=models.Count('contributorachievement')).order_by('-achievements','repository__name')

    def thumb_url(self, size=80):
        if not 'email' in self.extra_data or not self.extra_data['email']:
            return ''

        email_md5 = hashlib.md5(self.extra_data['email'].lower()).hexdigest()
        return 'http://www.gravatar.com/avatar/%s?s=%s' % (email_md5, size)

    @property
    def thumb_url_200_pixels(self):
        return self.thumb_url(200)

    @property
    def processed_commits(self):
        commits = 0
        for contrib in self.user.contributor_set.all():
            commits += contrib.total_commits
        return commits

    @property
    def added_lines(self):
        lines = 0
        for contrib in self.user.contributor_set.all():
            lines += contrib.added_lines
        return lines

    @property
    def removed_lines(self):
        lines = 0
        for contrib in self.user.contributor_set.all():
            lines += contrib.removed_lines
        return lines

    @property
    def total_repos(self):
        return len(self.user.contributor_set.all())

    @property
    def total_badges(self):
        badges = 0
        for contrib in self.user.contributor_set.all():
            badges += len(contrib.contributorachievement_set.all())
        return badges

    @property
    def other_users(self):
        return BadgerProfile.objects.order_by('?').exclude(slug=self.slug)[:50]


