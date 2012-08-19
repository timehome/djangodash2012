#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re

from social_auth.signals import pre_update
from django.dispatch import receiver
from social_auth.backends.contrib.github import GithubBackend

from repository.models import Repository, Contributor
from badger.badges.processor import RepositoryWorker

from pygithub3 import Github
from pyres import ResQ

@receiver(pre_update, sender=GithubBackend)
def user_update_callback(sender, user, response, details, **kwargs):
    profile = user.badgerprofile_set.get_or_create()[0]
    profile.extra_data = response
    profile.slug = response['login']
    profile.save()

    logging.info(u'Preparing data to put in queue for user [%s]' % response['email'])

    gh = Github(login=user.email, token=response['access_token'])

    for repo in gh.repos.list().all():
        try:
            repo_owner, repo_name = re.search('github.com\/(\w+)\/(\w+)', repo.html_url).groups()
            add_repository_to_queue(user, repo_owner, repo_name, repo_object=repo)
        except:
            logging.info('cannot be able to process repository %s ...' % repo.html_url)

def add_repository_to_queue(user, repo_owner, repository_name, repo_object=None):
    res = ResQ()
    repo = None
    token = user.get_profile().extra_data['access_token']

    if not repo_object:

        gh = Github(login=user.email, token=token)

        repo = gh.repos.get(repo_owner, repository_name)
    else:
        repo = repo_object

    queue_data = {'email': user.email, 'token': token}
    queue_data['repo'] = {
        'name': repo.name,
        'url': repo.url,
        'git_url': repo.git_url,
        'html_url': repo.html_url,
        'language': repo.language
    }

    db_repo, created = Repository.objects.get_or_create(
            git_url=repo.git_url, defaults=queue_data['repo'])

    query_filter = {'user': user, 'repository': db_repo}
    query_filter.update({'defaults': {
            'user': user,
            "repository": db_repo
        }
    })

    as_contributor, created = Contributor.objects.get_or_create(**query_filter)

    # put a timestamp field in repository model to verify if there is need to 
    # process again. so only put in queue if is not created and timestamp > x time

    res.enqueue(RepositoryWorker, queue_data)

