# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Car(models.Model):
	uid = models.CharField(max_length=100)
	speed = models.CharField(max_length=50)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	date = models.DateTimeField(auto_now=True)
	latitude_old = models.CharField(max_length=50)
	longitude_old = models.CharField(max_length=50)


class Credential(models.Model):
	uid = models.CharField(max_length=100)
	tokenId = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True)
	

class Configuration(models.Model):
	uid = models.CharField(max_length=100)
	alertAccident = models.BooleanField()
	alertStatus = models.BooleanField()
	alertSpeed = models.BooleanField()
	alertHelp = models.BooleanField()
	alertEvent = models.BooleanField()
	alertCurve = models.BooleanField()
	date = models.DateTimeField(auto_now=True)

class Sensor(models.Model):
	nid = models.CharField(max_length=100)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	frozen_road = models.BooleanField()
	dangerous_curve = models.BooleanField()
	date = models.DateTimeField(auto_now=True)
	
class Alert(models.Model):
	sender = models.CharField(max_length=100)
	receiver = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now=True)
	time = models.CharField(max_length=100)
