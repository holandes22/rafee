from django.conf.urls import patterns, url

from rafee.teams.views import TeamListAPIView, TeamDetailAPIView


urlpatterns = patterns(
    'rafee.teams',
    url(r'^$', TeamListAPIView.as_view(), name='team-list'),
    url(r'^(?P<id>\d+)$', TeamDetailAPIView.as_view(), name='team-detail'),
)
