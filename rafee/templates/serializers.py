from rest_framework.serializers import Serializer, CharField


class TemplateRenderSerializer(Serializer):

    template_name = CharField()
