# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vvs_map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stop',
            name='locality',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
