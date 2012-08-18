from django.views.generic import DetailView
from user_profile.models import BadgerProfile

class ProfileDetailView(DetailView):
    template_name = "profile/detail.html"
    model = BadgerProfile
