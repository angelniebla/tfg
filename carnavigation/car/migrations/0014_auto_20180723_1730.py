# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-23 15:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0013_delete_map'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Credentials',
            new_name='Credential',
        ),
    ]