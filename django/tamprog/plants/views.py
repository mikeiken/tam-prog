from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import *
from .models import Plant, BedPlant
from .serializers import PlantSerializer, BedPlantSerializer
from .services import *
from fertilizer.models import Fertilizer
from logging import getLogger

log = getLogger(__name__)

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
                description='Successful response',
                response=PlantSerializer(many=True)
            )
        },
    )
    def list(self, request, *args, **kwargs):
        ascending = request.query_params.get('asc', 'true').lower() == 'true'
        plants = PlantService.get_sorted_plants(ascending)
        serializer = self.get_serializer(plants, many=True)
        log.debug('Listing all plants')
        return Response(serializer.data)

    @extend_schema(
        summary='Search for plants by query',
        description='Search for plants using a query string. The search is case-insensitive and can match any part of the plant name or description.',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='List of plants matching the search query',
                response=PlantSerializer(many=True)
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Invalid query if the search string is empty or incorrect',
            ),
        },
        parameters=[
            OpenApiParameter(
                name='q',
                type=str,
                description='Search query (plant name or description)',
                required=True,
            ),
        ]
    )
    @action(detail=False, methods=['get'])    
    def search(self, request):
        query = request.query_params.get('q', '').lower()
        if not query:
            log.warning('Search query is required')
            return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)

        plants = PlantService.fuzzy_search(query)
        if not plants:
            log.info('No plants found matching the query')
            return Response({'message': 'No plants found matching the query'}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(plants, many=True)
        log.debug(f'Found {len(plants)} plants for query: {query}')
        return Response(serializer.data)
    
    @extend_schema(
        summary='Get search suggestions for plants',
        description='Get plant suggestions based on a query string. This endpoint returns a list of suggestions for autocomplete or partial search.',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='List of plant suggestions based on the query',
                response=str
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Invalid query if the search string is empty or incorrect',
            )
        },
        parameters=[
            OpenApiParameter(
                name='q',
                type=str,
                description='Query string for suggestions (partial plant name)',
                required=True,
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        query = request.query_params.get('q', '').lower()
        if not query:
            log.warning('Query string is required')
            return Response({'error': 'Query string is required'}, status=status.HTTP_400_BAD_REQUEST)

        suggestions = PlantService.get_suggestions(query)
        if not suggestions:
            log.info('No suggestions found for the given query')
            return Response({'message': 'No suggestions found for the given query'}, status=status.HTTP_200_OK)

        log.debug(f'Found {len(suggestions)} suggestions for query: {query}')
        return Response(suggestions)

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
        log.debug('Creating a new plant')
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Get a plant by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
                response=PlantSerializer
            )
        },
    )
    def retrieve(self, request, *args, **kwargs):
        log.debug('Retrieving a plant by ID')
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Partially update a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful update',
            )
        },
        parameters=PlantParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        log.debug('Partially updating a plant')
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update a plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful update',
            )
        },
        parameters=PlantParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        log.debug('Updating a plant')
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
        log.debug('Deleting a plant')
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
        log.debug('Deleting a bed plant')
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
        log.debug('Planting a new plant in a bed')
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary='Get all planted plants',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
                response=BedPlantSerializer(many=True)
            )
        },
    )
    def list(self, request, *args, **kwargs):
        log.debug('Listing all planted plants')
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary='Get a planted plant by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
                response=BedPlantSerializer
            )
        },
    )
    def retrieve(self, request, *args, **kwargs):
        log.debug('Retrieving a planted plant by ID')
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update a planted plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful update',
            )
        },
        parameters=BedPlantParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        log.debug('Updating a planted plant')
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Partially update a planted plant',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful update',
            )
        },
        parameters=BedPlantParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        log.debug('Partially updating a planted plant')
        return super().partial_update(request, *args, **kwargs)

    def perform_create(self, serializer):
        bed = serializer.validated_data['bed']
        plant = serializer.validated_data['plant']
        BedPlantService.plant_in_bed(bed, plant)
        log.info(f"Plant {plant.name} planted in bed with ID={bed.id}")

    @extend_schema(
        summary='Harvest a plant',
        description='Harvest a plant from a bed',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Plant harvested',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Plant not found',
            ),
        },
    )
    @action(detail=True, methods=['post'])
    def harvest(self, request, pk=None):
        bed_plant = self.get_object()
        BedPlantService.harvest_plant(bed_plant)
        log.info("Plant harvested")
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
        log.debug(f"Fertilizing plant {plant_name} with {fertilizer.name}")
        return BedPlantService.fertilize_plant(bed_plant, fertilizer)

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
        log.debug("Watering plants is not implemented yet")
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
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Plant not found',
                examples=[
                    OpenApiExample(
                        name='Plant not found',
                        value={'error': 'Plant not found'}
                    )
                ]
            ),
        },
    )
    @action(detail=True, methods=['post'])
    def dig_up(self, request, pk=None):
        bed_plant = self.get_object()
        log.debug("Digging up a plant")
        return BedPlantService.dig_up_plant(bed_plant)


    def get_queryset(self):
        fertilizer_applied = self.request.query_params.get('fertilizer_applied', None)
        if fertilizer_applied is not None:
            log.debug(f"Filtering bed plants by fertilizer_applied={fertilizer_applied}")
            return BedPlantService.filter_bed_plants(fertilizer_applied=fertilizer_applied.lower() == 'true')
        log.debug("Listing all bed plants")
        return BedPlant.objects.all()