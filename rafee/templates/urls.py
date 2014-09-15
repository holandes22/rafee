from django.conf.urls import patterns, url

from rafee.templates.views import TemplateListAPIView


urlpatterns = patterns(
    'rafee.templates',
    url(r'^$', TemplateListAPIView.as_view(), name='template-list'),
)
