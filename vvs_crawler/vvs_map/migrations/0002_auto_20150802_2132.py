# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vvs_map', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapentry',
            name='latitude_before',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mapentry',
            name='longitude_before',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
