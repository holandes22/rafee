import factory
from factory.django import DjangoModelFactory

from rafee.repositories.models import GitRepository


class GitRepositoryFactory(DjangoModelFactory):

    class Meta:
        model = GitRepository

    url = factory.Sequence(lambda x: 'http://git.com/{}'.format(x))
