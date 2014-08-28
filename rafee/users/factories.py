import factory
from factory.django import DjangoModelFactory
from django.conf import settings

from rafee.teams.factories import TeamFactory


class UserFactory(DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('email',)

    team = factory.SubFactory(TeamFactory)
    full_name = 'Gerardo Daniel Martino'
    email = factory.Sequence(lambda x: 'tata.martino{}@nob.com'.format(x))
