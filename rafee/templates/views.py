import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rafee.templates.tasks import render
from rafee.templates.manager import TemplateManager
from rafee.templates.permissions import IsAllowedToSeeTemplate
from rafee.templates.serializers import TemplateRenderSerializer
from rafee.templates.serializers import TemplatePreviewSerializer


class TemplateListAPIView(APIView):

    def get(self, request):
        manager = TemplateManager(settings.RAFEE_REPO_DIR)
        info = manager.get_templates_info()
        return Response(info)


class TemplateRenderAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated, IsAllowedToSeeTemplate)
    serializer_class = TemplateRenderSerializer

    def post(self, request):
        # TODO: Move validation to a base method
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        template_name = request.POST.get('template_name', None)
        # TODO: Verify template_name even exists
        task = render.delay(template_name)
        return Response({'task': task.task_id})


class TemplatePreviewAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TemplatePreviewSerializer

    # TODO: Add tests
    def post(self, request):
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        template_str = request.POST.get('template_str', None)
        manager = TemplateManager(settings.RAFEE_REPO_DIR)
        data_source = {}
        data_source_url = request.POST.get('data_source_url', None)
        if data_source_url is not None and data_source_url != '':
            data_source = requests.get(data_source_url).json()

        preview = manager.render_from_string(
            template_str,
            data_source=data_source,
        )
        return Response({'preview': preview})
