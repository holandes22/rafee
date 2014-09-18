import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError

from rafee.messages import TEMPLATE_NOT_FOUND
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


class TemplateAPIView(GenericAPIView):

    def validate(self, request):
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            raise ParseError(detail=serializer.errors)


class TemplateRenderAPIView(TemplateAPIView):

    permission_classes = (IsAuthenticated, IsAllowedToSeeTemplate)
    serializer_class = TemplateRenderSerializer

    def post(self, request):
        self.validate(request)
        template_name = request.POST.get('template_name')
        manager = TemplateManager(settings.RAFEE_REPO_DIR)
        if not manager.template_exists(template_name):
            return Response(
                {'detail': TEMPLATE_NOT_FOUND},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        task = render.delay(template_name)
        return Response({'task': task.task_id})


class TemplatePreviewAPIView(TemplateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TemplatePreviewSerializer

    def post(self, request):
        self.validate(request)
        template_str = request.POST.get('template_str')
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
