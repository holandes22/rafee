import factory
from factory.django import DjangoModelFactory
from django.conf import settings
from rest_framework.authtoken.models import Token


class UserFactory(DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('email',)

    full_name = 'Gerardo Daniel Martino'
    email = factory.Sequence(lambda x: 'tata.martino{}@nob.com'.format(x))
    username = factory.Sequence(lambda x: 'username{}'.format(x))
    password = '1'

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for team in extracted:
                self.teams.add(team)


class TokenFactory(DjangoModelFactory):

    class Meta:
        model = Token

    user = factory.SubFactory(UserFactory)
