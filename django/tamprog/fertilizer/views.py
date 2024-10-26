from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Fertilizer, BedPlantFertilizer
from .serializers import FertilizerSerializer, BedPlantFertilizerSerializer
from .services import create_fertilizer, get_fertilizers_for_plant

class FertilizerViewSet(viewsets.ModelViewSet):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        name = serializer.validated_data['name']
        growth_acceleration = serializer.validated_data['growth_acceleration']
        plant = serializer.validated_data['plant']
        create_fertilizer(name, growth_acceleration, plant)

class BedPlantFertilizerViewSet(viewsets.ModelViewSet):
    queryset = BedPlantFertilizer.objects.all()
    serializer_class = BedPlantFertilizerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        bed_plant = serializer.validated_data['bed_plant']
        fertilizer = serializer.validated_data['fertilizer']
        apply_fertilizer(bed_plant, fertilizer)

    @action(detail=True, methods=['get'])
    def fertilizers(self, request, pk=None):
        plant = self.get_object()
        fertilizers = get_fertilizers_for_plant(plant)
        serializer = FertilizerSerializer(fertilizers, many=True)
        return Response(serializer.data)
