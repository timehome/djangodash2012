from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from badger.views import IndexView, ProfileView
from badger.badges import initialize_badge_classes

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

initialize_badge_classes()

urlpatterns = patterns('',
    (r'^$', IndexView.as_view()),
    (r'^profile/?$', ProfileView.as_view()),

    url(r'^auth/', include('social_auth.urls')),

)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
