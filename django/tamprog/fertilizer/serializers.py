from rest_framework import serializers
from .models import Fertilizer, BedPlantFertilizer

class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = "__all__"

class BedPlantFertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedPlantFertilizer
        fields = "__all__"
