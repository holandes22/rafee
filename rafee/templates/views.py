import requests
from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jinja2 import Template

from rafee.slideshows.models import Slideshow
from rafee.templates.tasks import render
from rafee.templates.manager import TemplateManager
from rafee.templates.serializers import TemplateRenderSerializer


class TemplateListAPIView(GenericAPIView):

    def get(self, request):
        manager = TemplateManager(settings.RAFEE_REPO_DIR)
        info = manager.get_templates_info()
        return Response(info)


class TemplateRenderAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TemplateRenderSerializer

    def post(self, request):
        template_name = request.POST.get('template_name', None)
        if not template_name:
            return Response(
                # TODO: Copy validation error from DRF for consistency
                {'template_name': ['Missing parameter']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.user.is_staff:
            # Verify that the template belongs at least to one of the
            # user's slideshows, if not return Forbidden
            found = False
            teams = request.user.teams.all()
            slideshows = Slideshow.objects.filter(team__in=teams)
            for slideshow in slideshows:
                if template_name in slideshow.templates:
                    found = True
                    break
            if not found:
                return Response(status=status.HTTP_403_FORBIDDEN)

        task = render.delay(template_name)
        return Response({'task': task.task_id})


class TemplatePreviewAPIView(GenericAPIView):

    # TODO: Add tests
    def post(self, request):
        template_str = request.POST.get('template', None)
        # return 400 if no template
        data_source_url = request.POST.get('data_source_url', None)
        manager = TemplateManager(settings.RAFEE_REPO_DIR)
        template = Template(template_str)
        data_source = {}
        if data_source_url is not None:
            r = requests.get(data_source_url)
            data_source = r.json()
        return manager.render_template(template, data_source=data_source)
