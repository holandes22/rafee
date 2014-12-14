from rest_framework import serializers
from django.conf import settings

from rafee.messages import TEMPLATES_NOT_FOUND
from rafee.templates.manager import TemplateManager
from rafee.slideshows.models import Slideshow


class SlideshowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slideshow

    def validate_templates(self, value):
        manager = TemplateManager(settings.RAFEE_REPO_DIR)
        bad_template_names = []
        for template_name in value.split(','):
            if not manager.template_exists(template_name):
                bad_template_names.append(template_name)
        if len(bad_template_names) > 0:
            raise serializers.ValidationError(
                TEMPLATES_NOT_FOUND.format(bad_template_names),
            )
        return value
