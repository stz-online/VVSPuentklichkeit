# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vvs_map', '0002_stop_locality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='line_text',
            field=models.CharField(unique=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='stop',
            name='name',
            field=models.CharField(unique=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='vvsjourney',
            name='vvs_id',
            field=models.IntegerField(unique=True),
        ),
    ]
