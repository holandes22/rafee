from django.conf.urls import patterns, url

from rafee.slideshows.views import SlideshowListAPIView, SlideshowDetailAPIView


urlpatterns = patterns(
    'rafee.slideshows',
    url(r'^$', SlideshowListAPIView.as_view(), name='slideshow-list'),
    url(
        r'^(?P<id>\d+)$',
        SlideshowDetailAPIView.as_view(),
        name='slideshow-detail',
    ),
)
