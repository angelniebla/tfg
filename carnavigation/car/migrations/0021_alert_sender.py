# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-06 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0020_auto_20180802_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='sender',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]