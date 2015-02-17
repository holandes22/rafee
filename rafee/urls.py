from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework import routers

from rafee.tasks.views import TaskDetail
from rafee.slideshows.views import SlideshowViewSet
from rafee.templates.views import TemplateListAPIView
from rafee.templates.views import TemplateRenderAPIView
from rafee.templates.views import TemplatePreviewAPIView
from rafee.users.views import UserProfileAPIView
from rafee.users.views import UserViewSet

# pylint: disable=invalid-name


api_urlpatterns = patterns(
    '',
    url(
        r'docs/', include('rest_framework_swagger.urls')
    ),
    url(
        r'auth-token',
        'rest_framework_jwt.views.obtain_jwt_token',
        name='auth-token',
    ),
    url(r'teams/', include('rafee.teams.urls')),
    url(r'repositories/', include('rafee.repositories.urls')),
    url(r'templates/$', TemplateListAPIView.as_view(), name='template-list'),
    url(
        r'templates/preview$',
        TemplatePreviewAPIView.as_view(),
        name='template-preview',
    ),
    url(r'slide/$', TemplateRenderAPIView.as_view(), name='template-render'),
    url(
        r'tasks/(?P<task_id>[a-z0-9\-]+)',
        TaskDetail.as_view(),
        name='task-detail',
    ),
    url(r'^users/profile/$', UserProfileAPIView.as_view(), name='user-profile')
)


router = routers.SimpleRouter()
router.register(r'slideshows', SlideshowViewSet, base_name='slideshow')
router.register(r'users', UserViewSet)

api_urlpatterns += router.urls

urlpatterns = patterns(
    '',
    url(
        r'^{}/'.format(settings.API_PREFIX),
        include(api_urlpatterns),
    )
)

if settings.DEBUG:
    # Allow login via DRF browsable API
    urlpatterns += patterns(
        '',
        url(
            r'^api-auth/',
            include('rest_framework.urls', namespace='rest_framework'),
        ),
    )
