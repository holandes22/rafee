from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rafee.users.permissions import IsAdminUserOrReadOnly
from rafee.slideshows.models import Slideshow
from rafee.slideshows.serializers import SlideshowSerializer


class BaseSlideshowAPIView(object):

    model = Slideshow
    lookup_field = 'id'
    serializer_class = SlideshowSerializer
    permission_classes = (IsAuthenticated, IsAdminUserOrReadOnly)

    def get_queryset(self):
        if self.request.user.is_admin:
            return self.model._default_manager.all()
        else:
            return self.model._default_manager.filter(
                team__in=self.request.user.teams.all(),
            )


class SlideshowListAPIView(BaseSlideshowAPIView, ListCreateAPIView):

    pass


class SlideshowDetailAPIView(BaseSlideshowAPIView, RetrieveUpdateDestroyAPIView):
    pass
