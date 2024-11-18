from rest_framework import serializers
from .models import Plant, BedPlant

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

class BedPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedPlant
        fields = '__all__'
