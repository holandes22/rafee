from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from rafee.teams.models import Team


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=200, default='')
    team = models.ForeignKey(Team, related_name='users')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
