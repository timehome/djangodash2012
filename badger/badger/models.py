from django.db.models.signals import post_save
from django.dispatch import receiver
from social_auth.db.django_models import UserSocialAuth

from pygithub3 import Github
from pyres import ResQ

@receiver(post_save, sender=UserSocialAuth)
def user_save_callback(sender,instance, created, **kwargs):
    if instance.extra_data:
        user = {'email':instance.user.email, 'token': instance.extra_data['access_token']}
        gh = Github(login=user['email'], token=user['token'])

        for repo in gh.repos.list().all():
            user['repo'] = {'name': repo.name, 'url': repo.git_url}
            print user
            # ResQ.enqueue_from_string('Repository', 'repo_queue', user)