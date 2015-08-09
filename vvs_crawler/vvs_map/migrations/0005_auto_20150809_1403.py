# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vvs_map', '0004_auto_20150809_1344'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MapEntry',
        ),
        migrations.AddField(
            model_name='vvsdata',
            name='is_at_stop',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
