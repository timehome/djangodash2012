from django.views.generic import DetailView
from user_profile.models import BadgerProfile

class ProfileDetailView(DetailView):
    template_name = "profile/detail.html"

    def get_object(self):
        return BadgerProfile.objects.filter(user__id=self.kwargs['pk'])[0]
