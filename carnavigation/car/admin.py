# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from car.models import *

# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
	list_display = ('id', 'uid', 'speed', 'latitude', 'longitude', 'x', 'y', 'z', 'latitude_dst', 'longitude_dst')

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
	list_display = ('uid', 'alertAccident', 'alertStatus', 'alertSpeed', 'alertHelp', 'alertEvent', 'alertCurve')
	
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
	list_display = ('latitude', 'longitude', 'frozen_road', 'dangerous_curve')
