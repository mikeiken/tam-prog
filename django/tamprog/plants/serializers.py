from rest_framework import serializers
from .models import Plant, BedPlant

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

class BedPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedPlant
        fields = ['id', 'bed', 'plant', 'planted_at', 'fertilizer_applied', 'growth_time', 'growth_percentage', 'remaining_growth_time', 'is_harvested']
        read_only_fields = ['growth_time', 'is_harvested', 'planted_at', 'fertilizer_applied', 'growth_percentage', 'remaining_growth_time', 'is_grown']
