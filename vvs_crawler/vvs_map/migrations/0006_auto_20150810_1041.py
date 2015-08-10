# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vvs_map', '0005_auto_20150809_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vvsjourney',
            name='vvs_id',
            field=models.IntegerField(unique=True),
        ),
    ]
