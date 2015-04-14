from rest_framework.serializers import ModelSerializer, EmailField

from rafee.users.models import User


class UserSerializer(ModelSerializer):

    email = EmailField(allow_blank=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'teams', 'is_staff')
