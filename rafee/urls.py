from django.conf.urls import patterns, include, url
from django.conf import settings

from rafee.tasks.views import TaskDetail
from rafee.templates.views import TemplateListAPIView
from rafee.templates.views import TemplateRenderAPIView
from rafee.templates.views import TemplatePreviewAPIView

api_prefix = settings.API_PREFIX

urlpatterns = patterns(
    '',
    url(r'^{}/docs/'.format(api_prefix), include('rest_framework_swagger.urls')),
    url(r'^{}/auth-token'.format(api_prefix), 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^{}/users/'.format(api_prefix), include('rafee.users.urls')),
    url(r'^{}/teams/'.format(api_prefix), include('rafee.teams.urls')),
    url(r'^{}/slideshows/'.format(api_prefix), include('rafee.slideshows.urls')),
    url(r'^{}/repositories/'.format(api_prefix), include('rafee.repositories.urls')),
    url(
        r'^{}/templates/'.format(api_prefix),
        TemplateListAPIView.as_view(),
        name='template-list',
    ),
    url(
        r'^{}/templates/preview'.format(api_prefix),
        TemplatePreviewAPIView.as_view(),
        name='template-preview',
    ),
    url(
        r'^{}/slide'.format(api_prefix),
        TemplateRenderAPIView.as_view(),
        name='template-render',
    ),
    url(
        r'^{}/tasks/(?P<task_id>[a-z0-9\-]+)'.format(api_prefix),
        TaskDetail.as_view(),
        name='task-detail',
    ),
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
