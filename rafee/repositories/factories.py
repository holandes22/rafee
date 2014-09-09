import factory
from factory.django import DjangoModelFactory

from rafee.repositories.models import Repository


class RepositoryFactory(DjangoModelFactory):

    class Meta:
        model = Repository

    url = factory.Sequence(lambda x: 'http://git.com/{}'.format(x))
