from django.db import models


class Repository(models.Model):

    url = models.URLField(max_length=300, unique=True)
