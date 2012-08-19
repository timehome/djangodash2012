from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from badger.views import IndexView, new_repository_view, logout_view
from badger.badges import initialize_badge_classes

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

initialize_badge_classes()

urlpatterns = patterns('',
    (r'^$', IndexView.as_view()),
    url(r'^profile\/', include('user_profile.urls')),
    url(r'^auth\/', include('social_auth.urls')),
    url(r'^new-repo/?', new_repository_view),
    url(r'^logout/?', logout_view)

)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
