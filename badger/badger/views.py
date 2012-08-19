#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import TemplateView
from user_profile.models import BadgerProfile
from repository.models import Repository

from badger.models import add_repository_to_queue

class IndexView(TemplateView):
    template_name = "badger/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['users'] = BadgerProfile.objects.order_by('-user__date_joined')[:12]
        context['users_count'] = BadgerProfile.objects.count()
        context['repository_count'] = Repository.objects.count()
        return context

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def new_repository_view(request):
    if 'repo' in request.REQUEST:
        repository_url = request.REQUEST['repo']
        repo_owner, repo_name = re.search('github.com\/(\w+)\/(\w+)', repository_url).groups()
        add_repository_to_queue(request.user, repo_owner, repo_name)
    return redirect('/')


