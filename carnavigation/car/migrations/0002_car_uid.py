# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-19 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='uid',
            field=models.CharField(default='aaaa', max_length=100),
            preserve_default=False,
        ),
    ]
