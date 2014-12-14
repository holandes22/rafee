from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView

from rafee.repositories.tasks import remove_repo
from rafee.repositories.tasks import clone_and_create_repo
from rafee.repositories.models import Repository
from rafee.repositories.serializers import RepositorySerializer


class RepositoryListAPIView(ListCreateAPIView):

    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = clone_and_create_repo.delay(request.data['url'])
        return Response({'task': task.task_id})


class RepositoryDetailAPIView(RetrieveDestroyAPIView):

    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()

    def destroy(self, request, *args, **kwargs):
        task = remove_repo.delay(self.kwargs['pk'])
        return Response({'task': task.task_id})
