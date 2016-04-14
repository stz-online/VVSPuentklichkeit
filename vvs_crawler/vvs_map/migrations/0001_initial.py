# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('line_text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('vvs_id', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=300)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='VVSData',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('timestamp_before', models.DateTimeField()),
                ('coordinates_before', django.contrib.gis.db.models.fields.PointField(srid=4326, help_text='Represented as (longitude, latitude)', null=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(help_text='Represented as (longitude, latitude)', srid=4326)),
                ('delay', models.IntegerField()),
                ('is_at_stop', models.BooleanField()),
                ('real_time_available', models.BooleanField()),
                ('current_stop', models.ForeignKey(to='vvs_map.Stop', related_name='current_stop')),
                ('next_stop', models.ForeignKey(to='vvs_map.Stop', related_name='next_stop')),
            ],
        ),
        migrations.CreateModel(
            name='VVSJourney',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('day_of_operation', models.DateTimeField()),
                ('vvs_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VVSTransport',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('journey_id', models.IntegerField()),
                ('operator', models.TextField()),
                ('mod_code', models.IntegerField()),
                ('product_id', models.CharField(max_length=300)),
                ('direction', models.ForeignKey(to='vvs_map.Direction')),
                ('line', models.ForeignKey(to='vvs_map.Line')),
            ],
        ),
        migrations.AddField(
            model_name='vvsjourney',
            name='vvs_transport',
            field=models.ForeignKey(to='vvs_map.VVSTransport'),
        ),
        migrations.AddField(
            model_name='vvsdata',
            name='vvs_journey',
            field=models.ForeignKey(to='vvs_map.VVSJourney'),
        ),
        migrations.AlterUniqueTogether(
            name='vvstransport',
            unique_together=set([('direction', 'line', 'journey_id')]),
        ),
    ]
