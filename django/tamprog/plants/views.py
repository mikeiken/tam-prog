from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import *
from .models import Plant, BedPlant
from .serializers import PlantSerializer, BedPlantSerializer
from .services import *
from fertilizer.models import Fertilizer

from drf_spectacular.utils import extend_schema, extend_schema_view, \
    OpenApiResponse, OpenApiParameter, OpenApiExample

def PlantParameters(required=False):
    return [
        OpenApiParameter(
            name='name',
            type=str,
            description='Plant name',
            required=required,
        ),
        OpenApiParameter(
            name='growth_time',
            type=int,
            description='Growth time of plant',
            required=required,
        ),
        OpenApiParameter(
            name='price',
            type=float,
            description='Plant price',
            required=required,
        ),
        OpenApiParameter(
            name='description',
            type=str,
            description='Plant description',
            required=required,
        ),
    ]

@extend_schema(tags=['Plant'])
class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [AgronomistPermission]

    @extend_schema(
        summary='List all available plants',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
                response=PlantSerializer(many=True)
            )
        },
    )
    def list(self, request, *args, **kwargs):
        ascending = request.query_params.get('asc', 'true').lower() == 'true'
        plants = PlantService.get_sorted_plants(ascending)
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary='Create a new plant',
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description='Plant created successfully',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request',
            ),
        },
        parameters=PlantParameters(required=True),
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Get a plant by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
                response=PlantSerializer
            )
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Partially update a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull update',
            )
        },
        parameters=PlantParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull update',
            )
        },
        parameters=PlantParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Delete a plant',
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description='Plant deleted successfully',
            )
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

def BedPlantParameters(required=False):
    return [
        OpenApiParameter(
            name='ferilizer_applied',
            type=bool,
            description='Is created bed plant fertilized',
            required=required,
        ),
        OpenApiParameter(
            name='growth_time',
            type=int,
            description='Growth time of plant',
            required=required,
        ),
        OpenApiParameter(
            name='bed',
            type=int,
            description='Bed ID',
            required=required,
        ),
        OpenApiParameter(
            name='plant',
            type=int,
            description='Plant ID',
            required=required,
        ),
    ]

@extend_schema(tags=['Plant'])
class BedPlantViewSet(viewsets.ModelViewSet):
    queryset = BedPlant.objects.all()
    serializer_class = BedPlantSerializer
    permission_classes = [AgronomistOrRenterPermission, IsAuthenticated]

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary='Plant a new plant in a bed',
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description='Plant planted successfully',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request',
            ),
        },
        parameters=BedPlantParameters(required=True),    
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary='Get all planted plants',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
                response=BedPlantSerializer(many=True)
            )
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary='Get a planted plant by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull response',
                response=BedPlantSerializer
            )
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update a planted plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull update',
            )
        },
        parameters=BedPlantParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Partially update a planted plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successfull update',
            )
        },
        parameters=BedPlantParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def perform_create(self, serializer):
        bed = serializer.validated_data['bed']
        plant = serializer.validated_data['plant']
        BedPlantService.plant_in_bed(bed, plant)

    @extend_schema(
        summary='Harvest a plant',
        description='Harvest a plant from a bed',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Plant harvested',
            )
        },
    )
    @action(detail=True, methods=['post'])
    def harvest(self, request, pk=None):
        bed_plant = self.get_object()
        BedPlantService.harvest_plant(bed_plant)
        return Response({'status': 'plant harvested'})

    @extend_schema(
        summary='Fertilize a plant',
        description='Fertilize a plant in a bed',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Plant fertilized',
                examples=[
                    OpenApiExample(
                        name='Fertilized plant',
                        value={'status': 'plant fertilized'},
                    )
                ]
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='No suitable fertilizer found',
                examples=[
                    OpenApiExample(
                        name='No suitable fertilizer',
                        value={'error': 'No suitable fertilizer found'},
                    )
                ]
            ),
        },
    )
    @action(detail=True, methods=['post'])
    def fertilize(self, request, pk=None):
        bed_plant = self.get_object()
        plant_name = bed_plant.plant.name
        fertilizer = Fertilizer.objects.filter(compound__icontains=plant_name).first()
        if not fertilizer:
            return Response({'error': 'No suitable fertilizer found'}, status=status.HTTP_400_BAD_REQUEST)
        BedPlantService.fertilize_plant(bed_plant, fertilizer)
        return Response({'status': 'plant fertilized'})

    @extend_schema(
        summary='Water a plant',
        description='Water a plant in a bed',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Plant watered',
                examples=[
                    OpenApiExample(
                        name='Watered plant',
                        value={'status': 'plant watered'},
                    )
                ]
            )
        },
    )
    @action(detail=True, methods=['post'])
    def water(self, request, pk=None):
        bed_plant = self.get_object()
        BedPlantService.water_plant(bed_plant)
        return Response({'status': 'plant watered'})

    @extend_schema(
        summary='Dig up a plant',
        description='Dig up a plant from a bed',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Plant dug up',
                examples=[
                    OpenApiExample(
                        name='Dug up plant',
                        value={'status': 'plant dug up'},
                    )
                ]
            )
        },
    )
    @action(detail=True, methods=['delete'])
    def dig_up(self, request, pk=None):
        bed_plant = self.get_object()
        BedPlantService.dig_up_plant(bed_plant)
        return Response({'status': 'plant dug up'})

    def get_queryset(self):
        fertilizer_applied = self.request.query_params.get('fertilizer_applied', None)
        if fertilizer_applied is not None:
            return BedPlantService.filter_bed_plants(fertilizer_applied=fertilizer_applied.lower() == 'true')
        return BedPlant.objects.all()