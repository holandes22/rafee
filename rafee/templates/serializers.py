from rest_framework import serializers


class TemplateRenderSerializer(serializers.Serializer):

    template_name = serializers.CharField()


class TemplatePreviewSerializer(serializers.Serializer):

    template_str = serializers.CharField()
    data_source_url = serializers.URLField(
        required=False,
        allow_blank=True,
    )
