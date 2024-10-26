from rest_framework import serializers
from .models import Person, Agronomist, Worker

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'wallet_balance', 'full_name', 'phone_number']

class AgronomistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agronomist
        fields = ['id', 'name']

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'name']
