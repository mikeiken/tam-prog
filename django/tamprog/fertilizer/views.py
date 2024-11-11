from rest_framework import viewsets, status
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

    @extend_schema(
        summary='Get fertilizers applied to a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
                response=BedPlantFertilizerSerializer(many=True)
            )
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Apply fertilizer to a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
            )
        },
        parameters=[
            OpenApiParameter(
                name='bed_plant',
                description='Bed plant ID',
                type=int,
                required=True,
            ),
            OpenApiParameter(
                name='fertilizer',
                description='Fertilizer ID',
                type=int,
                required=True,
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Update fertilizer applied to a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
            )
        },
        parameters=[
            OpenApiParameter(
                name='bed_plant',
                description='Bed plant ID',
                type=int,
            ),
            OpenApiParameter(
                name='fertilizer',
                description='Fertilizer ID',
                type=int,
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='Delete fertilizer applied to a plant',
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description='Successfull response',
            )
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary='Get fertilizer applied to a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
                response=BedPlantFertilizerSerializer
            )
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update fertilizer applied to a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
            )
        },
        parameters=[
            OpenApiParameter(
                name='bed_plant',
                description='Bed plant ID',
                type=int,
                required=True,
            ),
            OpenApiParameter(
                name='fertilizer',
                description='Fertilizer ID',
                type=int,
                required=True,
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary='Get fertilizers applied to a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
                response=BedPlantFertilizerSerializer(many=True)
            )
        },
    )
    @action(detail=True, methods=['get'])
    def fertilizers(self, request, pk=None):
        bed_plant = self.get_object()
        fertilizers = FertilizerService.get_fertilizers_for_plant(bed_plant)
        serializer = BedPlantFertilizerSerializer(fertilizers, many=True)
        return Response(serializer.data)
