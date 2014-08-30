from rest_framework.serializers import ModelSerializer

from rafee.teams.models import Team


class TeamSerializer(ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name', 'users')
