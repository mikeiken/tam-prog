from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Fertilizer, BedPlantFertilizer
from .serializers import FertilizerSerializer, BedPlantFertilizerSerializer
from .services import create_fertilizer, get_fertilizers_for_plant, apply_fertilizer

class FertilizerViewSet(viewsets.ModelViewSet):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        name = serializer.validated_data['name']
        boost = serializer.validated_data['boost']
        compound = serializer.validated_data['compound']
        create_fertilizer(name, boost, compound)

class BedPlantFertilizerViewSet(viewsets.ModelViewSet):
    queryset = BedPlantFertilizer.objects.all()
    serializer_class = BedPlantFertilizerSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        bed_plant = serializer.validated_data['bed_plant']
        fertilizer = serializer.validated_data['fertilizer']
        apply_fertilizer(bed_plant, fertilizer)

    @action(detail=True, methods=['get'])
    def fertilizers(self, request, pk=None):
        bed_plant = self.get_object()
        fertilizers = get_fertilizers_for_plant(bed_plant)
        serializer = FertilizerSerializer(fertilizers, many=True)
        return Response(serializer.data)
