import random

import factory
from factory.django import DjangoModelFactory
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.module_loading import import_string


NAMES = [
    u'Sergio Almiron',
    u'Sergio Batista',
    u'Ricardo Enrique',
    u'Claudio Borghi',
    u'Jose Luis Brown',
    u'Daniel Passarella',
    u'Jorge Burruchaga',
    u'Nestor Clausen',
    u'Jose Luis Cuciuffo',
    u'Diego Maradona',
    u'Jorge Valdano',
    u'Hector Enrique',
    u'Oscar Garre',
    u'Ricardo Giusti',
    u'Luis Islas',
    u'Julio Olarticoechea',
    u'Pedro Pasculli',
    u'Nery Pumpido',
    u'Oscar Ruggeri',
    u'Carlos Daniel Tapia',
    u'Marcelo Trobbiani',
    u'Hector Miguel Zelada',
]


class UserFactory(DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('email',)

    full_name = factory.Sequence(lambda x: random.choice(NAMES) + str(x))
    email = factory.LazyAttribute(
        lambda o: '{}@afa.com'.format(o.full_name.replace(' ', '.').lower())
    )
    username = factory.Sequence(lambda x: 'username{}'.format(x))
    password = make_password(
        '1',
        hasher=import_string(settings.PASSWORD_HASHERS[0])().algorithm)

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for team in extracted:
                self.teams.add(team)
