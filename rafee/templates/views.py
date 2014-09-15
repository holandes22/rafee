from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from rafee.templates.manager import TemplateManager


class TemplateListAPIView(APIView):

    def get(self, request):
        manager = TemplateManager(settings.RAFEE_REPO_DIR)
        info = manager.get_templates_info()
        return Response(info)


class SlideRenderAPIView(APIView):

    def post(self, request):
        template_name = request.DATA.get('template_name', None)
        if not template_name:
            # Raise validation error, return 400
            pass


class SlideRenderPreviewAPIView(APIView):
    pass
