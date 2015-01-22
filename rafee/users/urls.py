from django.conf.urls import patterns, url
from rest_framework import routers

from rafee.users.views import UserProfileAPIView
from rafee.users.views import UserViewSet

# pylint: disable=invalid-name

router = routers.SimpleRouter()
router.register(r'', UserViewSet)


urlpatterns = patterns(
    'rafee.users',
    url(r'^/profile/$', UserProfileAPIView.as_view(), name='user-profile'),
)

urlpatterns += router.urls
