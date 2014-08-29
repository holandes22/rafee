import factory
from factory.django import DjangoModelFactory

from rafee.teams.models import Team


class TeamFactory(DjangoModelFactory):

    class Meta:
        model = Team

    name = factory.Sequence(lambda x: 'Team {}'.format(x))
