from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Fertilizer, BedPlantFertilizer
from .permission import *
from .serializers import FertilizerSerializer, BedPlantFertilizerSerializer
from .services import FertilizerService

from drf_spectacular.utils import extend_schema, extend_schema_view, \
    OpenApiResponse, OpenApiParameter, OpenApiExample

def FertilizerParameters(required=False):
    return [
        OpenApiParameter(
            name="name",
            description="Fertilizer name",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="boost",
            description="Fertilizer boost",
            type=int,
            required=required,
        ),
        OpenApiParameter(
            name="compound",
            description="Fertilizer compound",
            type=str,
            required=required,
        ),
    ]

@extend_schema(tags=['Fertilizer'])
class FertilizerViewSet(viewsets.ModelViewSet):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    permission_classes = [AgronomistPermission]

    @extend_schema(
        summary='Get all fertilizers',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
                response=FertilizerSerializer(many=True)
            )
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Get fertilizer by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
                response=FertilizerSerializer
            )
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Create fertilizer',
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description='Successful response',
            )
        },
        parameters=FertilizerParameters(required=True),
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Update fertilizer',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
            )
        },
        parameters=FertilizerParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Partially update fertilizer',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
            )
        },
        parameters=FertilizerParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Delete fertilizer',
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description='Successful response',
            )
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        name = serializer.validated_data['name']
        boost = serializer.validated_data['boost']
        compound = serializer.validated_data['compound']
        FertilizerService.create_fertilizer(name, boost, compound)

def BedPlantFertilizerParameters(required=False):
    return [
        OpenApiParameter(
            name="bed_plant",
            description="Bed plant ID",
            type=int,
            required=required,
        ),
        OpenApiParameter(
            name="fertilizer",
            description="Fertilizer ID",
            type=int,
            required=required,
        ),
    ]

@extend_schema(tags=['Fertilizer', 'Plant'])
class BedPlantFertilizerViewSet(viewsets.ModelViewSet):
    queryset = BedPlantFertilizer.objects.all()
    serializer_class = BedPlantFertilizerSerializer
    permission_classes = [BedPlantF]

    @extend_schema(
        summary='Get fertilizers applied to all plants',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
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
                description='Successful response',
            )
        },
        parameters=BedPlantFertilizerParameters(required=True),
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Update fertilizer applied to a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
            )
        },
        parameters=BedPlantFertilizerParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='Delete fertilizer applied to a plant',
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description='Successful response',
            )
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary='Get fertilizer applied to a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
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
                description='Successful response',
            )
        },
        parameters=BedPlantFertilizerParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)