# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vvs_map', '0003_auto_20150809_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='vvsdata',
            name='vvs_journey',
            field=models.ForeignKey(default=None, to='vvs_map.VVSJourney'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vvsjourney',
            name='vvs_transport',
            field=models.ForeignKey(default=1, to='vvs_map.VVSTransport'),
            preserve_default=False,
        ),
    ]
