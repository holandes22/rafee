from django.conf.urls import patterns, include, url
from django.conf import settings


api_prefix = settings.API_PREFIX

urlpatterns = patterns(
    '',
    url(r'^{}/docs/'.format(api_prefix), include('rest_framework_swagger.urls')),
    url(r'^{}/users/'.format(api_prefix), include('rafee.users.urls')),
    url(r'^{}/teams/'.format(api_prefix), include('rafee.teams.urls')),
    url(r'^{}/slideshows/'.format(api_prefix), include('rafee.slideshows.urls')),
)
