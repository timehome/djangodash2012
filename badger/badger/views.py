from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "badger/index.html"

class ProfileView(TemplateView):
    template_name = "profile/profile.html"
