# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-10 14:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0022_sensor_nid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='latitude_dst',
        ),
        migrations.RemoveField(
            model_name='car',
            name='longitude_dst',
        ),
        migrations.RemoveField(
            model_name='car',
            name='x',
        ),
        migrations.RemoveField(
            model_name='car',
            name='y',
        ),
        migrations.RemoveField(
            model_name='car',
            name='z',
        ),
    ]