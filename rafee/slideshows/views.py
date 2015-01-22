from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rafee.users.permissions import IsAdminUserOrReadOnly
from rafee.slideshows.models import Slideshow
from rafee.slideshows.serializers import SlideshowSerializer

# pylint: disable=protected-access


class SlideshowViewSet(ModelViewSet):

    model = Slideshow
    lookup_field = 'id'
    lookup_value_regex = r'\d+'
    serializer_class = SlideshowSerializer
    permission_classes = (IsAuthenticated, IsAdminUserOrReadOnly)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model._default_manager.all()
        else:
            return self.model._default_manager.filter(
                team__in=self.request.user.teams.all(),
            )
