from django.conf.urls import patterns, url

from rafee.users.views import UserListAPIView, UserDetailAPIView

urlpatterns = patterns(
    'rafee.users',
    url(r'^$', UserListAPIView.as_view(), name='user-list'),
    url(
        r'^(?P<email>[\w.-]+@[\w.-]+\.[A-Za-z]+)$',
        UserDetailAPIView.as_view(),
        name='user-detail',
    ),
)
