from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Fertilizer, BedPlantFertilizer
from .permission import *
from .serializers import FertilizerSerializer, BedPlantFertilizerSerializer
from .services import FertilizerService

from drf_spectacular.utils import extend_schema, extend_schema_view, \
    OpenApiResponse, OpenApiParameter, OpenApiExample

@extend_schema(tags=['Fertilizer'])
class FertilizerViewSet(viewsets.ModelViewSet):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    permission_classes = [AgronomistPermission]

    def perform_create(self, serializer):
        name = serializer.validated_data['name']
        boost = serializer.validated_data['boost']
        compound = serializer.validated_data['compound']
        FertilizerService.create_fertilizer(name, boost, compound)

@extend_schema(tags=['Bed'])
class BedPlantFertilizerViewSet(viewsets.ModelViewSet):
    queryset = BedPlantFertilizer.objects.all()
    serializer_class = BedPlantFertilizerSerializer
    permission_classes = [BedPlantF]

    @action(detail=True, methods=['get'])
    def fertilizers(self, request, pk=None):
        bed_plant = self.get_object()
        fertilizers = FertilizerService.get_fertilizers_for_plant(bed_plant)
        serializer = BedPlantFertilizerSerializer(fertilizers, many=True)
        return Response(serializer.data)
