# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from car.models import *
from django.conf import settings
from car.forms import PollsForm


from django.forms import Widget

# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
	list_display = ('id', 'uid', 'speed', 'latitude', 'longitude', 'latitude_old', 'longitude_old','date')
	search_fields = ('id',)


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
	list_display = ('uid', 'alertAccident', 'alertStatus', 'alertSpeed', 'alertHelp', 'alertEvent', 'alertCurve', 'date')
	
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
	list_display = ('nid', 'latitude', 'longitude', 'frozen_road', 'dangerous_curve', 'date')

@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
	list_display = ('uid', 'tokenId', 'date')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
	list_display = ('sender','receiver', 'title', 'description', 'date')
