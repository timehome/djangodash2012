from social_auth.signals import pre_update
from django.dispatch import receiver
from social_auth.backends.contrib.github import GithubBackend

from badger.badges.processor import RepositoryWorker

from pygithub3 import Github
from pyres import ResQ

@receiver(pre_update, sender=GithubBackend)
def user_update_callback(sender, user, response, details, **kwargs):
    profile = user.badgerprofile_set.get_or_create()[0]
    profile.extra_data = response
    profile.save()

    user = {'email':response['email'], 'token': response['access_token']}
    gh = Github(login=user['email'], token=user['token'])

    res = ResQ()
    for repo in gh.repos.list().all():
        user['repo'] = {'name': repo.name, 'url': repo.git_url}
        res.enqueue(RepositoryWorker, user)
