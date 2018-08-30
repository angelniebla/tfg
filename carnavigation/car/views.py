# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from math import radians, cos, sin, asin, sqrt
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from car.models import Car
from car.models import Credential
from car.models import Configuration
from car.models import Sensor
from car.models import Alert
from car.serializers import CarSerializer
from car.serializers import CredentialSerializer
from car.serializers import ConfigurationSerializer
from car.serializers import SensorSerializer
import requests
import json
from django.utils import timezone
import time

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
	if request.method == 'POST':
		start = time.time()
		data = JSONParser().parse(request)
		data_old = None
		print data['uid']
		for x in Car.objects.all():
			if x.uid == data['uid']:
				if data['latitude'] == x.latitude and data['longitude'] == x.longitude:
					data['latitude_old'] = x.latitude_old
					data['longitude_old'] = x.longitude_old
				else:
					data['latitude_old'] = x.latitude
					data['longitude_old'] = x.longitude
				
				x.delete()
		serializer = CarSerializer(data=data)
		if serializer.is_valid():
			if authorize(data['uid']):
				serializer.save()
				processData(data, start)
				finish = time.time() - start
				#print 'finish: ' + str(finish)
				return JSONResponse(serializer.data, status=201)
			return JSONResponse({'status': False, 'message': "Usuario no registrado"}, status=401)
		return JSONResponse(serializer.errors, status=400)
		

def authorize(uid):
	l = filter(lambda y: y.uid == uid, Credential.objects.all())
	return len(l) != 0
	

def notSend(uid, to):
	count = Alert.objects.all().count()
	if count > 10:
		 alerts = Alert.objects.all()[count-10:]
	elif count >= 0:
		alerts = Alert.objects.all()[:]
	else:
		return False
	for alert in alerts:
		if(uid == alert.sender and to == alert.receiver and alert.date.strftime("%Y-%m-%d %H:%M") == timezone.now().strftime("%Y-%m-%d %H:%M")):
			return True
	
	return False

		
def processData(car1, start):
	if(len(Car.objects.all()) > 1):
		for x in Credential.objects.all():
			if car1['uid'] != x.uid:
				if not(notSend(car1['uid'], x.uid)):
					car2 = filter(lambda y: y.uid == x.uid, Car.objects.all())
					if len(car2) > 0:
						if float(car1['speed']) < 90:
							radius_max = 0.25 # kilometros
						else:
							radius_max = 0.40
						radius_min = 0.14
						distance = haversine(float(car1['latitude']), float(car1['longitude']), float(car2[0].latitude), float(car2[0].longitude))	#Distancia entre los dos coches
						print distance
						if distance <= radius_max and distance > radius_min:
							if nearby(float(car1['latitude']), float(car1['longitude']), float(car1['latitude_old']), float(car1['longitude_old']), float(car2[0].latitude), float(car2[0].longitude), float(car2[0].latitude_old), float(car2[0].longitude_old)):
								print 'near'
								carConfiguration = filter(lambda y: y.uid == x.uid, Configuration.objects.all())
								direction = get_direction(float(car1['latitude']), float(car1['longitude']), float(car2[0].latitude), float(car2[0].longitude), float(car1['latitude_old']), float(car1['longitude_old']), float(car2[0].latitude_old), float(car2[0].longitude_old))
								print direction
								isBehind = behind(float(car1['latitude']), float(car1['longitude']), float(car2[0].latitude), float(car2[0].longitude), float(car1['latitude_old']), float(car1['longitude_old']), direction)
								send_alert(x.tokenId, isBehind, carConfiguration[0], distance, car1['speed'],direction, car1['uid'], start)
							else:
								print 'far'
						else:
							print 'lejos'

def haversine(lat1, lon1, lat2, lon2):
    """
    cálculo de la distancia de círculo máximo entre dos puntos de un globo 
    sabiendo su longitud y su latitud.
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
			
def nearby(lat1, lon1, lat1_old, lon1_old, lat2, lon2, lat2_old, lon2_old):
	"""
	Comprobacion de si el coche2 esta mas cerca del coche1 
	que en un momento anterior
    """
	dis = haversine(lat2,lon2,lat1, lon1)
	dis_old = haversine(lat2_old,lon2_old,lat1_old,lon1_old)
	
	if(dis < dis_old):
		return True
	else:
		return False


def behind(lat1, lon1, lat2, lon2, lat1_old, lon1_old, direction):
	"""
    Comprobacion de si el coche2 esta detras del coche1 
    """
	if(direction == 0):
		d_lat1 = lat1-lat1_old
		d_lon1 = lon1-lon1_old
		d_lat = lat2-lat1
		d_lon = lon2-lon1
		
		if(d_lat1 > 0 and d_lon1 > 0): 	
			if(d_lat > 0 and d_lon > 0):
				return True
			else:
				return False
		elif(d_lat1 < 0 and d_lon1 < 0): 
			if(d_lat < 0 and d_lon < 0):
				return True
			else:
				return False
		elif(d_lat1 > 0 and d_lon1 < 0): 
			if(d_lat > 0 and d_lon < 0):
				return True
			else:
				return False
		elif(d_lat1 < 0 and d_lon1 > 0): 		
			if(d_lat < 0 and d_lon > 0):
				return True
			else:
				return False	
	else:
		return None
			
				
def get_direction(lat1, lon1, lat2, lon2, lat1_old, lon1_old, lat2_old, lon2_old):
	"""
	Calculo de la direccion de un coche respecto a otro                                                                              
	0 -> Misma direccion
	1 -> Direcciones opuestas
	2 -> Direcciones que se cruzan
    """
	d_lat1 = lat1-lat1_old
	d_lon1 = lon1-lon1_old
	d_lat2 = lat2-lat2_old
	d_lon2 = lon2-lon2_old
	
	if(d_lat1 > 0 and d_lon1 > 0): 
		if(d_lat2 < 0 and d_lon2 < 0):
			return 1
		elif(d_lat2 > 0 and d_lon2 < 0):
			return 2
		elif(d_lat2 < 0 and d_lon2 > 0):
			return 2
		elif(d_lat2 > 0 and d_lon2 > 0):
			return 0
	elif(d_lat1 < 0 and d_lon1 < 0): 
		if(d_lat2 > 0 and d_lon2 > 0):
			return 1
		elif(d_lat2 > 0 and d_lon2 < 0):
			return 2
		elif(d_lat2 < 0 and d_lon2 > 0):
			return 2
		elif(d_lat2 < 0 and d_lon2 < 0):
			return 0
	elif(d_lat1 > 0 and d_lon1 < 0): 
		if(d_lat2 > 0 and d_lon2 > 0):
			return 2
		elif(d_lat2 < 0 and d_lon2 < 0):
			return 2
		elif(d_lat2 < 0 and d_lon2 > 0):
			return 1
		elif(d_lat2 > 0 and d_lon2 < 0): 
			return 0
	elif(d_lat1 < 0 and d_lon1 > 0): 
		if(d_lat2 > 0 and d_lon2 > 0):
			return 2
		elif(d_lat2 < 0 and d_lon2 < 0):
			return 2
		elif(d_lat2 > 0 and d_lon2 < 0):
			return 1
		elif(d_lat2 < 0 and d_lon2 > 0): 
			return 0
		
def send_alert(to, behind, carConfiguration, distance, speed, direction, uid, start):
	if(direction == 0 and carConfiguration.alertAccident):
		if(behind != None):
			if(behind):
				body = {"to": to, "data": {"title": "ALERTA POR POSIBLE COLISION TRASERA","body": "Un coche a " + str(distance*1000)[:3] + " metros se aproxima a " + speed + " k/h por detras"}}
				postNotification(body, uid, start)
	
	elif(direction == 1 and carConfiguration.alertAccident):
		body = {"to": to, "data": {"title": "ALERTA POR POSIBLE COLISION DELATERA","body": "Un coche a " + str(distance*1000)[:3] + " metros se aproxima a " + speed + " k/h por delante"}}
		postNotification(body, uid, start)
	
	elif(direction == 2 and carConfiguration.alertHelp):
		body = {"to": to, "data": {"title": "ALERTA POR VEHICULO APROXIMANDOSE A INTERSECCION","body": "Un coche a " + str(distance*1000)[:3] + " metros se aproxima a " + speed + " k/h en la interseccion"}}
		postNotification(body, uid, start)

def postNotification(body, uid, start):
	print body
	
	headers = {"content-type": "application/json", "Authorization": "key=AAAApRo1WOU:APA91bFro_aJI-puTK_zRwdMtPnNxgfQPbrC0QE6qaMjpHHAvYXnhhAUI3Pposz8fQJfE3GgxXv1J0i1SsmnHFSETOZQ-0V6QjuUZaQRij9UwE1St7C1I7xMcLtNApGe0_NPc0EkNBgG"}
	url = "https://fcm.googleapis.com/fcm/send"
	requests.post(url, data = json.dumps(body), headers=headers)
	credential = filter(lambda y: y.tokenId == body['to'], Credential.objects.all())
	Alert.objects.create(sender = uid, receiver = credential[0].uid,title = body['data']['title'], description = body['data']['body'], time = str(time.time() - start)).save()
	
	
@csrf_exempt
def credential_list(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		for x in Credential.objects.all():
			if x.uid == data['uid']:
				x.delete()
		serializer = CredentialSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
		
@csrf_exempt
def configuration_list(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		for x in Configuration.objects.all():
			if x.uid == data['uid']:
				x.delete()
		serializer = ConfigurationSerializer(data=data)
		if serializer.is_valid():
			if authorize(data['uid']):
				serializer.save()
				return JSONResponse(serializer.data, status=201)
			return JSONResponse({'status': False, 'message': "Usuario no registrado"}, status=401)
		return JSONResponse(serializer.errors, status=400)
		

@csrf_exempt
def sensor(request):
	if request.method == 'POST':
		start = time.time()
		data = JSONParser().parse(request)
		for x in Sensor.objects.all():
			if x.nid == data['nid']:
				x.delete()
		serializer = SensorSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			if data['frozen_road'] or data['dangerous_curve']:
				processDataSensor(data)
			finish = time.time() - start
			print 'finish: ' + str(finish)
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
				
def processDataSensor(sensor):
	if(len(Car.objects.all()) > 0):
		for x in Credential.objects.all():
			car = filter(lambda y: y.uid == x.uid, Car.objects.all())
			if len(car) > 0:
				radius = 5.00 # kilometros
				distance = haversine(float(sensor['latitude']), float(sensor['longitude']), float(car[0].latitude), float(car[0].longitude))	#Distancia entre el coche y el sensor
				if distance <= radius:
					print car[0].uid
					isNear = nearby(float(car[0].latitude), float(car[0].longitude),float(car[0].latitude_old), float(car[0].longitude_old),float(sensor['latitude']), float(sensor['longitude']),float(sensor['latitude']), float(sensor['longitude']))
					print isNear
					if isNear:
						carConfiguration = filter(lambda y: y.uid == x.uid, Configuration.objects.all())
						send_alert_sensor(sensor, distance, carConfiguration, x.tokenId)		
						
					
def send_alert_sensor(sensor, distance, carConfiguration, to):
	if sensor['frozen_road'] and carConfiguration[0].alertStatus:
		body = {"to": to, "data": {"title": "ALERTA POR POSIBLE CARRETERA CONGELADA","body": "Un tramo de la carretera a " + str(distance)[:3] + " kilometros puede estar congelado"}}

	if sensor['dangerous_curve'] and carConfiguration[0].alertCurve:
		body = {"to": to, "data": {"title": "ALERTA POR CURVA PELIGROSA","body": "Una curva a " + str(distance)[:3] + " kilometros se encuentra a oscuras"}}
		
	if(body != None):
		postNotification(body, sensor['nid'])
