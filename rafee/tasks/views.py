from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rafee.celery import app


class TaskDetail(APIView):

    permission_classes = (IsAuthenticated,)

    # pylint: disable=no-self-use,unused-argument
    def get(self, request, task_id):
        result = app.AsyncResult(task_id)

        data = {'id': task_id, 'status': result.status}
        if result.ready():
            if result.failed():
                data['result'] = str(result.get(propagate=False))
                data['traceback'] = result.traceback
            else:
                data['result'] = result.result

        return Response(data)
