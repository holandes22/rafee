from django.db import models
from django.contrib.auth.models import AbstractUser

from rafee.teams.models import Team


class User(AbstractUser):

    full_name = models.CharField(max_length=200, default='')
    team = models.ForeignKey(Team, related_name='users')
