from rest_framework.serializers import ModelSerializer

from rafee.users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'team', 'is_admin')
