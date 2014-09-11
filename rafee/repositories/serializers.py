from rest_framework.serializers import ModelSerializer

from rafee.repositories.models import Repository


class RepositorySerializer(ModelSerializer):

    class Meta:
        model = Repository
        fields = ('id', 'url')
