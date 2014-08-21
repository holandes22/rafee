# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GitRepository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polling_interval', models.PositiveIntegerField(default=30)),
                ('url', models.URLField(unique=True, max_length=300)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
