from django.conf.urls import patterns, url

from rafee.repositories.views import RepositoryListAPIView, RepositoryDetailAPIView


urlpatterns = patterns(
    'rafee.repositories',
    url(r'^$', RepositoryListAPIView.as_view(), name='repository-list'),
    url(r'^(?P<id>\d+)$', RepositoryDetailAPIView.as_view(), name='repository-detail'),
)
