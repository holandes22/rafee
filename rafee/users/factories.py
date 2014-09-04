import factory
from factory.django import DjangoModelFactory
from django.conf import settings


class UserFactory(DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('email',)

    full_name = 'Gerardo Daniel Martino'
    email = factory.Sequence(lambda x: 'tata.martino{}@nob.com'.format(x))

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for team in extracted:
                self.teams.add(team)
