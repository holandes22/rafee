import factory
from factory.django import DjangoModelFactory
from django.conf import settings

from rafee.teams.factories import TeamFactory


class UserFactory(DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    team = factory.SubFactory(TeamFactory)
    username = 'tata'
    first_name = 'Gerardo'
    last_name = 'Martino'
    full_name = 'Gerardo Daniel Martino'
    is_staff = False
    is_superuser = False
    email = factory.LazyAttribute(
        lambda a: '{}.{}@example.com'.format(
            a.first_name,
            a.last_name
        ).lower()
    )
