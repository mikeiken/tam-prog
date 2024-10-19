from rest_framework import serializers
from .models import *
from django.utils import timezone

class AgronomistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agronomist
        fields = "__all__"

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"


class GardenBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = GardenBed
        fields = "__all__"


class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = "__all__"
    def create(self, validated_data):
        validated_data['landing_data'] = timezone.now().date()  # Устанавливаем текущую дату
        return super().create(validated_data)


class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class AvailablePlantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailablePlants
        fields = "__all__"
    def create(self, validated_data):
        validated_data['landing_data'] = timezone.now().date()  # Устанавливаем текущую дату
        return super().create(validated_data)