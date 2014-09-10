from rest_framework.serializers import ModelSerializer

from rafee.users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'teams', 'is_staff')
