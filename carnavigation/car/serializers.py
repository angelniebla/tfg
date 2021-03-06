from rest_framework import serializers
from .models import Car
from .models import Credential
from .models import Configuration
from .models import Sensor

class CarSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only=True)
	uid = serializers.CharField()
	speed = serializers.CharField()
	latitude = serializers.CharField()
	longitude = serializers.CharField()
	latitude_old = serializers.CharField(default='0')
	longitude_old = serializers.CharField(default='0')
	
	def create(self, validated_data):
		return Car.objects.create(**validated_data)
		
	def update(self, instance, validated_data):
		instance.uid = validated_data.get('uid', instance.uid)
		instance.tokenId = validated_data.get('tokenId', instance.uid)
		instance.speed = validated_data.get('speed', instance.speed)
		instance.latitude = validated_data.get('latitude', instance.latitude)
		instance.longitude = validated_data.get('longitude', instance.longitude)
		instance.latitude_old = validated_data.get('latitude_old', instance.latitude_old)
		instance.longitude_old = validated_data.get('longitude_old', instance.longitude_old)
		instance.save()
		return instance
		
	class Meta:
		model = Car
		fields = ('id', 'uid', 'tokenId', 'speed', 'latitude', 'longitude','latitude_old', 'longitude_old')

class CredentialSerializer(serializers.Serializer):
	uid = serializers.CharField()
	tokenId = serializers.CharField()
	
	def create(self, validated_data):
		return Credential.objects.create(**validated_data)
		
	def update(self, instance, validated_data):
		instance.uid = validated_data.get('uid', instance.uid)
		instance.tokenId = validated_data.get('tokenId', instance.tokenId)
		instance.save()
		return instance
		
	class Meta:
		model = Credential
		fields = ('uid', 'tokenId')
		
		
class ConfigurationSerializer(serializers.Serializer):
	uid = serializers.CharField()
	alertAccident = serializers.BooleanField()
	alertStatus = serializers.BooleanField()
	alertSpeed = serializers.BooleanField()
	alertHelp = serializers.BooleanField()
	alertEvent = serializers.BooleanField()
	alertCurve = serializers.BooleanField()

	
	def create(self, validated_data):
		return Configuration.objects.create(**validated_data)
		
	def update(self, instance, validated_data):
		instance.uid = validated_data.get('uid', instance.uid)
		instance.alertAccident = validated_data.get('alertAccident', instance.alertAccident)
		instance.alertStatus = validated_data.get('alertStatus', instance.alertStatus)
		instance.alertSpeed = validated_data.get('alertSpeed', instance.alertSpeed)
		instance.alertHelp = validated_data.get('alertHelp', instance.alertHelp)
		instance.alertEvent = validated_data.get('alertEvent', instance.alertEvent)
		instance.alertCurve = validated_data.get('alertCurve', instance.alertCurve)
		instance.save()
		return instance
		
	class Meta:
		model = Configuration
		fields = ('uid', 'alertAccident', 'alertStatus', 'alertSpeed', 'alertHelp', 'alertEvent', 'alertCurve')
		
class SensorSerializer(serializers.Serializer):
	nid = serializers.CharField()
	latitude = serializers.CharField()
	longitude = serializers.CharField()
	frozen_road = serializers.BooleanField()
	dangerous_curve = serializers.BooleanField()

	
	def create(self, validated_data):
		return Sensor.objects.create(**validated_data)
		
	def update(self, instance, validated_data):
		instance.nid = validated_data.get('nid', instance.nid)
		instance.latitude = validated_data.get('latitude', instance.latitude)
		instance.longitude = validated_data.get('longitude', instance.longitude)
		instance.frozen_road = validated_data.get('frozen_road', instance.frozen_road)
		instance.dangerous_curve = validated_data.get('dangerous_curve', instance.dangerous_curve)
		instance.save()
		return instance
		
	class Meta:
		model = Sensor
		fields = ('nid', 'latitude', 'longitude', 'frozen_road', 'dangerous_curve')

