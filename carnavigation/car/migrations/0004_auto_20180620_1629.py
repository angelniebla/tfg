# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_car_tokenid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=100)),
                ('tokenId', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='car',
            name='tokenId',
        ),
    ]
