from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView

from rafee.repositories.tasks import clone_and_create_repo
from rafee.repositories.models import Repository
from rafee.repositories.serializers import RepositorySerializer


class RepositoryListAPIView(ListCreateAPIView):

    model = Repository
    serializer_class = RepositorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.DATA,
            files=request.FILES,
        )

        if serializer.is_valid():
            task = clone_and_create_repo.delay(serializer.data['url'])
            return Response({'task': task.task_id})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RepositoryDetailAPIView(RetrieveDestroyAPIView):

    model = Repository
    serializer_class = RepositorySerializer
