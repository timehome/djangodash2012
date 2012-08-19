from django.conf.urls import patterns
from user_profile.views import ProfileDetailView

urlpatterns = patterns('',
    (r'(?P<slug>\w+)?$', ProfileDetailView.as_view())
)