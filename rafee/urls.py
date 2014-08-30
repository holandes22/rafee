from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^{}/users/'.format(settings.API_PREFIX), include('rafee.users.urls')),
    url(r'^{}/teams/'.format(settings.API_PREFIX), include('rafee.teams.urls')),
)
