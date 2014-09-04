from rest_framework.serializers import Field
from rest_framework.serializers import ModelSerializer

from rafee.users.models import User


class UserSerializer(ModelSerializer):

    id = Field(source='email')

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'teams', 'is_admin')
