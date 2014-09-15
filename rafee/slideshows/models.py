from django.db import models

from rafee.teams.models import Team


class Slideshow(models.Model):

    name = models.CharField(max_length=50)
    team = models.ForeignKey(Team)
    templates = models.CharField(max_length=1000)
    transition_interval = models.PositiveIntegerField(default=15)
    caching_interval = models.PositiveIntegerField(default=120)

    class Meta:
        unique_together = (('name', 'team'),)
