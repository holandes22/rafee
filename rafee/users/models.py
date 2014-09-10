from django.db import models
from django.contrib.auth.models import AbstractUser

from rafee.teams.models import Team


class User(AbstractUser):

    full_name = models.CharField(max_length=200, default='')
    teams = models.ManyToManyField(Team, related_name='users')

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email
