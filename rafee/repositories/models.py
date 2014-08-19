from django.db import models


class Repository(models.Model):

    file_path = models.FilePathField(max_length=200)
    polling_interval = models.PositiveIntegerField(default=30)

    class Meta:
        abstract = True


class GitRepository(Repository):

    url = models.URLField(max_length=300)

    class Meta:
        unique_together = (('url', 'file_path'),)
