# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-19 20:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0010_car_geometry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='geometry',
        ),
    ]
