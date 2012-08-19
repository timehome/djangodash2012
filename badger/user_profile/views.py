from django.views.generic import DetailView
from user_profile.models import BadgerProfile

class ProfileDetailView(DetailView):
    template_name = "profile/detail.html"
    model = BadgerProfile

    def get_object(self):
        import pdb;pdb.set_trace()
