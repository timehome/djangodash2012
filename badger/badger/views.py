from django.views.generic import TemplateView
from user_profile.models import BadgerProfile
from repository.models import Repository

class IndexView(TemplateView):
    template_name = "badger/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['users'] = BadgerProfile.objects.order_by('user__date_joined')[:12]
        context['users_count'] = BadgerProfile.objects.count()
        context['repository_count'] = Repository.objects.count()
        return context

