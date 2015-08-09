# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vvs_map', '0002_auto_20150802_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='VVSData',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('timestamp', models.DateTimeField()),
                ('timestamp_before', models.DateTimeField()),
                ('longitude', models.IntegerField()),
                ('longitude_before', models.IntegerField(null=True, blank=True)),
                ('latitude', models.IntegerField()),
                ('latitude_before', models.IntegerField(null=True, blank=True)),
                ('delay', models.IntegerField()),
                ('current_stop', models.CharField(max_length=300)),
                ('next_stop', models.CharField(max_length=300)),
                ('real_time_available', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='VVSJourney',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('day_of_operation', models.DateTimeField()),
                ('vvs_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VVSTransport',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('direction_text', models.CharField(max_length=300)),
                ('line_text', models.CharField(max_length=300)),
                ('journey_id', models.IntegerField()),
                ('operator', models.TextField()),
                ('mod_code', models.IntegerField()),
                ('product_id', models.CharField(max_length=300)),
            ],
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='current_stop',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='day_of_operation',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='journey_id',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='latitude_before',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='longitude_before',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='mod_code',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='next_stop',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='operator',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='real_time_available',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='timestamp_before',
        ),
        migrations.RemoveField(
            model_name='mapentry',
            name='vvs_id',
        ),
        migrations.AlterUniqueTogether(
            name='vvstransport',
            unique_together=set([('direction_text', 'line_text', 'journey_id')]),
        ),
    ]
