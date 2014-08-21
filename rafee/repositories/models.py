from django.db import models


class Repository(models.Model):

    polling_interval = models.PositiveIntegerField(default=30)

    class Meta:
        abstract = True


class GitRepository(Repository):

    url = models.URLField(max_length=300, unique=True)
