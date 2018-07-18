from django.db import models


class Car(models.Model):
	
	uid = models.CharField(max_length=100)
	tokenId = models.CharField(max_length=100)
	speed = models.CharField(max_length=50)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	
