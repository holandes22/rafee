from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rafee.teams.models import Team
from rafee.teams.serializers import TeamSerializer


class BaseTeamAPIView(object):

    model = Team
    lookup_field = 'id'
    serializer_class = TeamSerializer


class TeamListAPIView(BaseTeamAPIView, ListCreateAPIView):
    pass


class TeamDetailAPIView(BaseTeamAPIView, RetrieveUpdateDestroyAPIView):
    pass
