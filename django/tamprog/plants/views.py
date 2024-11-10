from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from fuzzywuzzy import fuzz
from .permissions import *
from .models import Plant, BedPlant
from .serializers import PlantSerializer, BedPlantSerializer
from .services import *
from fertilizer.models import Fertilizer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [AgronomistPermission]

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)
        if search_query:
            plants = self.fuzzy_search(search_query)
        else:
            ascending = request.query_params.get('asc', 'true').lower() == 'true'
            plants = PlantService.get_sorted_plants(ascending)
        
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)

    def fuzzy_search(self, query, threshold=70):
        results = []
        plants = Plant.objects.all()
        for plant in plants:
            similarity = fuzz.ratio(query.lower(), plant.name.lower())
            if similarity >= threshold:
                results.append(plant)
        return results


class BedPlantViewSet(viewsets.ModelViewSet):
    queryset = BedPlant.objects.all()
    serializer_class = BedPlantSerializer
    permission_classes = [AgronomistOrRenterPermission, IsAuthenticated]

    def perform_create(self, serializer):
        bed = serializer.validated_data['bed']
        plant = serializer.validated_data['plant']
        BedPlantService.plant_in_bed(bed, plant)

    @action(detail=True, methods=['post'])
    def harvest(self, request, pk=None):
        bed_plant = self.get_object()
        BedPlantService.harvest_plant(bed_plant)
        return Response({'status': 'plant harvested'})

    @action(detail=True, methods=['post'])
    def fertilize(self, request, pk=None):
        bed_plant = self.get_object()
        plant_name = bed_plant.plant.name
        fertilizer = Fertilizer.objects.filter(compound__icontains=plant_name).first()
        if not fertilizer:
            return Response({'error': 'No suitable fertilizer found'}, status=404)
        BedPlantService.fertilize_plant(bed_plant, fertilizer)
        return Response({'status': 'plant fertilized'})

    @action(detail=True, methods=['post'])
    def water(self, request, pk=None):
        bed_plant = self.get_object()
        BedPlantService.water_plant(bed_plant)
        return Response({'status': 'plant watered'})

    @action(detail=True, methods=['post'])
    def dig_up(self, request, pk=None):
        bed_plant = self.get_object()
        BedPlantService.dig_up_plant(bed_plant)
        return Response({'status': 'plant dug up'})

    def get_queryset(self):
        fertilizer_applied = self.request.query_params.get('fertilizer_applied', None)
        if fertilizer_applied is not None:
            return BedPlantService.filter_bed_plants(fertilizer_applied=fertilizer_applied.lower() == 'true')
        return BedPlant.objects.all()