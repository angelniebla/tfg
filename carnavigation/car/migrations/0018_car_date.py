# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-26 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0017_remove_car_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]