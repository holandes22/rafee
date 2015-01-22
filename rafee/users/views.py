from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveAPIView

from rest_framework.viewsets import ModelViewSet

from rafee.users.models import User
from rafee.users.serializers import UserSerializer


class BaseUserAPIView(object):

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserProfileAPIView(BaseUserAPIView, RetrieveAPIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(BaseUserAPIView, ModelViewSet):

    permission_classes = (IsAuthenticated, IsAdminUser)
