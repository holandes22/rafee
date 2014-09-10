from django.conf.urls import patterns, url

from rafee.users.views import UserListAPIView, UserDetailAPIView


urlpatterns = patterns(
    'rafee.users',
    url(r'^$', UserListAPIView.as_view(), name='user-list'),
    url(r'^(?P<pk>\d+)$', UserDetailAPIView.as_view(), name='user-detail'),
)
