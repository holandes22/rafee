import factory
from factory.django import DjangoModelFactory

from rafee.slideshows.models import Slideshow
from rafee.teams.factory import TeamFactory


class SlideshowFactory(DjangoModelFactory):

    class Meta:
        model = Slideshow

    name = factory.Sequence(lambda x: 'Slideshow{}'.format(x))
    team = factory.SubFactory(TeamFactory)
    templates = 't1,t2'
