from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rafee.users.models import User
from rafee.users.permissions import IsAdminUserOrReadOnly
from rafee.users.serializers import UserSerializer


class BaseUserAPIView(object):

    model = User
    serializer_class = UserSerializer


class UserListAPIView(BaseUserAPIView, ListCreateAPIView):
    pass


class UserDetailAPIView(BaseUserAPIView, RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, IsAdminUserOrReadOnly)
