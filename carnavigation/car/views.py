# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from math import radians, cos, sin, asin, sqrt
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from car.models import Car
from car.models import Credentials
from .models import Configuration
from .models import Sensor
from car.serializers import CarSerializer
from car.serializers import CredentialsSerializer
from car.serializers import ConfigurationSerializer
from car.serializers import SensorSerializer
import requests
import json


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def car_list(request):
	if request.method == 'GET':
		car = Car.objects.all()
		serializer = CarSerializer(car, many=True)
		return JSONResponse(serializer.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		data_old = None
		for x in Car.objects.all():
			if x.uid == data['uid']:
				data_old = x
				x.delete()
		serializer = CarSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			processData(data,data_old)
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
		
		
def processData(car1, car1_old):
	if(len(Car.objects.all()) > 1):
		for x in Credentials.objects.all():
			if car1['uid'] != x.uid:
				car2 = filter(lambda y: y.uid == x.uid, Car.objects.all())
				radius = 1.00 # kilometros
				distance = haversine(float(car1['latitude']), float(car1['longitude']), float(car2[0].latitude), float(car2[0].longitude))	#Distancia entre los dos coches
				if distance <= radius and car1_old != None:
					isBehind = behind(float(car1['latitude']), float(car1['longitude']), float(car2[0].latitude), float(car2[0].longitude), float(car1['latitude_dst']), float(car1['latitude_dst']))	#Comprobacion de si el coche2 esta destras del coche1 segun el destino marcado por el coche1
					if nearby(float(car1['latitude']), float(car1['longitude']), float(car1_old.latitude), float(car1_old.longitude), float(car2[0].latitude), float(car2[0].longitude)):	#Comprobacion de si el coche2 esta mas cerca del coche1 que antes
						print('esta cerca')
						carConfiguration = filter(lambda y: y.uid == x.uid, Configuration.objects.all())
						if(carConfiguration[0].alertAccident):
							send_alert_accident(float(car1['x']), float(car1['y']), float(car1['z']), float(car2[0].x), float(car2[0].y), float(car2[0].z), x.tokenId, isBehind)
					else:
						print('no esta cerca')


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # decimales a radianes 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radio de la tierra en kilometros.
    return c * r
			
def nearby(lat1, lon1, lat1_old, lon1_old, lat2, lon2):
	dis = haversine(lat2,lon2,lat1, lon1)
	dis_old = haversine(lat2,lon2,lat1_old,lon1_old)
	
	if(dis < dis_old):
		return True
	else:
		return False	

def behind(lat1, lon1, lat2, lon2, lat1_dst, lon1_dst):
	if(lat1_dst == 0 or lon1_dst == 0):
		return None
	else:
		dis1 = haversine(lat1,lon1,lat1_dst,lon1_dst)
		dis2 = haversine(lat2,lon2,lat1_dst,lon1_dst)
		
		if(dis1 < dis2):
			return True
		else:
			return False

def direction(x, y, z):
	if(y < -0.5):	#VERTICAL
		if(1 > z >= 0):
			return 0
		elif(z >= 2):
			return 3
		elif(z >= 1):
			return 1
		elif(z <= -1):
			return 2
	else:	#HORIZONTAL
		if(z > 0):	#DERECHA
			if(0 >= x > -2):
				return 0
			elif(x <= -2):
				return 1
			elif(2 > x > 0):
				return 2
			elif(x >= 2):
				return 3
		else:	#IZQUIERDA
			if(0 >= x > -2):
				return 3
			elif(x <= -2):
				return 2
			elif(2 > x > 0):
				return 1
			elif(x >= 2):
				return 0
			
def send_alert_accident(x1, y1, z1, x2, y2, z2, to, behind):
	
	print x1
	print y1
	print z1
	car1_dir = direction(x1,y1,z1)
	car2_dir = direction(x2,y2,z2)
	print car1_dir
	print car2_dir
	
	if(car1_dir == car2_dir):
		print behind
		if(behind != None):
			if(behind):
				body = {"to": to, "notification": {"title": "ALERTA POR POSIBLE COLISION TRASERA","body": "Un coche a x metros se aproxima a x k/h por detras"}}
			else:
				body = {"to": to, "notification": {"title": "HAY UN COCHE DELANTE","body": ""}}
		else:
			body = {"to": to, "notification": {"title": "HAY UN COCHE CERCA","body": ""}}				
	
	
	elif((car1_dir == 0 and car1_dir == 3) or (car1_dir == 3 and car2_dir == 0) or (car1_dir == 1 and car2_dir == 2) or (car1_dir == 2 and car2_dir == 1)):
		body = {"to": to, "notification": {"title": "ALERTA POR POSIBLE COLISION DELATERA","body": "Un coche a x metros se aproxima a x k/h por delante"}}
	
	else:
		body = {"to": to, "notification": {"title": "ALERTA POR VEHICULO APROXIMANDOSE A INTERSECCION","body": "Un coche a x metros se aproxima a x k/h en la interseccion"}}

	if(body != None):
		postNotification(body)

def postNotification(body):
	print body
	headers = {"content-type": "application/json", "Authorization": "key=AAAApRo1WOU:APA91bFro_aJI-puTK_zRwdMtPnNxgfQPbrC0QE6qaMjpHHAvYXnhhAUI3Pposz8fQJfE3GgxXv1J0i1SsmnHFSETOZQ-0V6QjuUZaQRij9UwE1St7C1I7xMcLtNApGe0_NPc0EkNBgG"}
	url = "https://fcm.googleapis.com/fcm/send"
	requests.post(url, data = json.dumps(body), headers=headers)
	
@csrf_exempt
def credential_list(request):
	if request.method == 'GET':
		credential = Credentials.objects.all()
		serializer = CredentialsSerializer(credential, many=True)
		return JSONResponse(serializer.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		for x in Credentials.objects.all():
			if x.uid == data['uid']:
				x.delete()
		serializer = CredentialsSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
		
@csrf_exempt
def configuration_list(request):
	if request.method == 'GET':
		configuration = Configuration.objects.all()
		serializer = ConfigurationSerializer(configuration, many=True)
		return JSONResponse(serializer.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		for x in Configuration.objects.all():
			if x.uid == data['uid']:
				x.delete()
		serializer = ConfigurationSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
		

@csrf_exempt
def sensor(request):
	if request.method == 'GET':
		sensor = Sensor.objects.all()
		serializer = SensorSerializer(sensor, many=True)
		return JSONResponse(serializer.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		for x in Sensor.objects.all():
			if x.latitude[:5] == data['latitude'][:5] and x.longitude[:5] == data['longitude'][:5]:
				x.delete()
		serializer = SensorSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			if data['frozen_road'] or data['dangerous_curve']:
				processDataSensor(data)
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
				
def processDataSensor(sensor):
	if(len(Car.objects.all()) > 1):
		for x in Credentials.objects.all():
			car = filter(lambda y: y.uid == x.uid, Car.objects.all())
			radius = 10.00 # kilometros
			distance = haversine(float(sensor['latitude']), float(sensor['longitude']), float(car[0].latitude), float(car[0].longitude))	#Distancia entre el coche y el sensor
			print float(sensor['latitude'])
			print float(sensor['longitude'])
			print float(car[0].latitude)
			print float(car[0].longitude)
			if distance <= radius:
					print('esta cerca')
					carConfiguration = filter(lambda y: y.uid == x.uid, Configuration.objects.all())
					send_alert_sensor(sensor, distance, carConfiguration, x.tokenId)		
			else:
				print('no esta cerca')
					
def send_alert_sensor(sensor, distance, carConfiguration, to):
	if sensor['frozen_road'] and carConfiguration[0].alertStatus:
		body = {"to": to, "notification": {"title": "ALERTA POR POSIBLE CARRETERA CONGELADA","body": "Un tramo de la carretera a " + str(distance)[:3] + " kilometros puede estar congelado"}}

	if sensor['dangerous_curve'] and carConfiguration[0].alertCurve:
		body = {"to": to, "notification": {"title": "ALERTA POR CURVA PELIGROSA","body": "Una curva a " + str(distance)[:3] + " kilometros se encuentra a oscuras"}}
		
	if(body != None):
		postNotification(body)
