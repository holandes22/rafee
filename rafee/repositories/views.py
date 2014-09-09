from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rafee.repositories.models import Repository
from rafee.repositories.serializers import RepositorySerializer


class BaseRepositoryAPIView(object):

    model = Repository
    lookup_field = 'id'
    serializer_class = RepositorySerializer


class RepositoryListAPIView(BaseRepositoryAPIView, ListCreateAPIView):
    pass


class RepositoryDetailAPIView(BaseRepositoryAPIView, RetrieveUpdateDestroyAPIView):
    pass
