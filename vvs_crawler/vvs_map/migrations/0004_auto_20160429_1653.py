# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vvs_map', '0003_auto_20160422_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='name',
            field=models.CharField(max_length=300, null=True, unique=True, blank=True),
        ),
    ]
