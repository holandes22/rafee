from rest_framework.serializers import ModelSerializer

from rafee.slideshows.models import Slideshow


class SlideshowSerializer(ModelSerializer):

    class Meta:
        model = Slideshow
