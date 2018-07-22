# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models as geomodels

# Create your models here.

class Car(models.Model):
	
	uid = models.CharField(max_length=100)
	speed = models.CharField(max_length=50)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	x = models.CharField(max_length=50)
	y = models.CharField(max_length=50)
	z = models.CharField(max_length=50)
	latitude_dst = models.CharField(max_length=50)
	longitude_dst = models.CharField(max_length=50)


class Credentials(models.Model):
	uid = models.CharField(max_length=100)
	tokenId = models.CharField(max_length=200)
	

class Configuration(models.Model):
	uid = models.CharField(max_length=100)
	alertAccident = models.BooleanField()
	alertStatus = models.BooleanField()
	alertSpeed = models.BooleanField()
	alertHelp = models.BooleanField()
	alertEvent = models.BooleanField()
	alertCurve = models.BooleanField()

class Sensor(models.Model):
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	frozen_road = models.BooleanField()
	dangerous_curve = models.BooleanField()
