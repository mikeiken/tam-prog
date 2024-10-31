from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import *
from .models import Plant, BedPlant
from .serializers import PlantSerializer, BedPlantSerializer
from .services import plant_in_bed, harvest_plant, fertilize_plant, water_plant, dig_up_plant
from fertilizer.models import Fertilizer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [AgronomistPermission]

class BedPlantViewSet(viewsets.ModelViewSet):
    queryset = BedPlant.objects.all()
    serializer_class = BedPlantSerializer
    permission_classes = [AgronomistOrRenterPermission, IsAuthenticated]

    def perform_create(self, serializer):
        bed = serializer.validated_data['bed']
        plant = serializer.validated_data['plant']
        plant_in_bed(bed, plant)

    @action(detail=True, methods=['post'])
    def harvest(self, request, pk=None):
        bed_plant = self.get_object()
        harvest_plant(bed_plant)
        return Response({'status': 'plant harvested'})

    @action(detail=True, methods=['post'])
    def fertilize(self, request, pk=None):
        bed_plant = self.get_object()
        plant_name = bed_plant.plant.name
        fertilizer = Fertilizer.objects.filter(compound__icontains=plant_name).first()
        if not fertilizer:
            return Response({'error': 'No suitable fertilizer found'}, status=404)
        fertilize_plant(bed_plant, fertilizer)
        return Response({'status': 'plant fertilized'})

    @action(detail=True, methods=['post'])
    def water(self, request, pk=None):
        bed_plant = self.get_object()
        water_plant(bed_plant)
        return Response({'status': 'plant watered'})

    @action(detail=True, methods=['post'])
    def dig_up(self, request, pk=None):
        bed_plant = self.get_object()
        dig_up_plant(bed_plant)
        return Response({'status': 'plant dug up'})
