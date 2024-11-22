from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .permission import *
from .models import Field, Bed
from .serializers import FieldSerializer, BedSerializer
from .services import *
from logging import getLogger

log = getLogger(__name__)

from drf_spectacular.utils import extend_schema, extend_schema_view, \
    OpenApiResponse, OpenApiParameter, OpenApiExample

def FieldParameters(required=False):
    return [
        OpenApiParameter(
            name="name",
            description="Field name",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="count_beds",
            description="Count of beds",
            type=int,
            required=required,
        ),
        OpenApiParameter(
            name="price",
            description="Field price",
            type=float,
            required=required,
        ),
    ]

@extend_schema(tags=['Field'])
class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [AgronomistPermission]

    def perform_create(self, serializer):
        log.debug(f"Creating field with data: {self.request.data}")
        count_beds = self.request.data.get('count_beds', 0)
        serializer.save(count_beds=count_beds)

    @extend_schema(
        summary='List all fields',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with list of fields',
                response=FieldSerializer(many=True),
            ),
        },
        parameters=[
            OpenApiParameter(
                name='sort',
                type=str,
                description='Sort by field',
                required=False,
                enum=['id', 'name', 'count_beds', 'price'],
            ),
            OpenApiParameter(
                name='asc',
                type=bool,
                description='Ascending order',
                required=False,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        sort_by = request.query_params.get('sort', 'price')
        ascending = request.query_params.get('asc', 'true').lower() == 'true'
        fields = FieldService.get_sorted_fields(sort_by, ascending)
        serializer = self.get_serializer(fields, many=True)
        log.debug(f"Returning list of fields: {serializer.data}")
        return Response(serializer.data)
    
    @extend_schema(
        summary='Retrieve field',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with field',
                response=FieldSerializer,
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        log.debug(f"Retrieving field with ID={kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update field',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with updated field',
            ),
        },
        parameters=FieldParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        log.debug(f"Updating field with ID={kwargs['pk']} with data: {request.data}")
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Partial update field',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with updated field',
            ),
        },
        parameters=FieldParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        log.debug(f"Partially updating field with ID={kwargs['pk']} with data: {request.data}")
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Destroy field',
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description='Successful response',
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        log.debug(f"Deleting field with ID={kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary='Create field',
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description='Successful response with created field',
            ),
        },
        parameters=FieldParameters(required=True),
    )
    def create(self, request, *args, **kwargs):
        log.debug(f"Creating field with data: {request.data}")
        return super().create(request, *args, **kwargs)

def BedParameters(required=False):
    return [
        OpenApiParameter(
            name="is_rented",
            description="Is bed rented",
            type=bool,
            required=required,
        ),
        OpenApiParameter(
            name="field",
            description="Field ID",
            type=int,
            required=required,
        ),
        OpenApiParameter(
            name="rented_by",
            description="User ID",
            type=int,
            required=required,
        ),
    ]

@extend_schema(tags=['Bed'])
class BedViewSet(viewsets.ModelViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Create bed',
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description='Successful response with created bed',
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        log.debug(f"Creating bed with data: {request.data}")
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='List all beds',
        description='List all beds',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with list of beds',
                response=BedSerializer(many=True),
            )
        },
    )
    def list(self, request, *args, **kwargs):
        log.debug(f"Listing all beds")
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary='Retrieve bed',
        description='Retrieve bed by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with bed',
                response=BedSerializer,
            )
        },
    )
    def retrieve(self, request, *args, **kwargs):
        log.debug(f"Retrieving bed with ID={kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update bed',
        description='Update bed by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with updated bed',
            )
        },
        parameters=BedParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        log.debug(f"Updating bed with ID={kwargs['pk']} with data: {request.data}")
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Destroy bed',
        description='Destroy bed by ID',
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description='Successful response',
            )
        },
    )
    def destroy(self, request, *args, **kwargs):
        log.debug(f"Deleting bed with ID={kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary='Partial update bed',
        description='Partial update bed by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with updated bed',
            )
        },
        parameters=BedParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        log.debug(f"Partially updating bed with ID={kwargs['pk']} with data: {request.data}")
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='List all beds for current user',
        description='List all beds that are rented by the current user',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with list of beds',
                response=BedSerializer(many=True),
            )
        },
    )
    @action(detail=False, methods=['get'])
    def my_beds(self, request):
        beds = BedService.get_user_beds(request.user)
        serializer = self.get_serializer(beds, many=True)
        log.debug(f"Returning list of beds rented by user: {serializer.data}")
        return Response(serializer.data)

    @extend_schema(
        summary='Rent bed',
        description='Rent bed',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Bed successfully rented.',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request: Bed is already rented.',
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Bed not found.',
            ),
        },
        parameters=BedParameters(required=True),
        examples=[
            OpenApiExample(
                name='Rent bed for user',
                value={
                    "is_rented": True,
                    "field": 1,
                    "rented_by": 1
                }
            )
        ],
    )
    @action(detail=True, methods=['post'])
    def rent(self, request, pk=None):
        bed = self.get_object()
        person = request.user
        log.debug(f"Renting bed with ID={bed.id} for user with ID={person.id}")
        return BedService.rent_bed(bed.id, person)

    @extend_schema(
        summary='Release bed',
        description='Release bed',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Bed successfully released.',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request: Bed is not rented.',
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Bed not found.',
            ),
        },
        parameters=BedParameters(required=True),
        examples=[
            OpenApiExample(
                name='Release bed for user',
                value={
                    "is_rented": False,
                    "field": 1,
                    "rented_by": 1
                }
            )
        ],
    )
    @action(detail=True, methods=['post'])
    def release(self, request, pk=None):
        bed = self.get_object()
        log.debug(f"Releasing bed with ID={bed.id}")
        return BedService.release_bed(bed.id)


    def get_queryset(self):
        is_rented = self.request.query_params.get('is_rented', None)
        if is_rented is not None:
            log.debug(f"Filtering beds by is_rented={is_rented}")
            return BedService.filter_beds(is_rented=is_rented.lower() == 'true')
        log.debug("Returning all beds")
        return Bed.objects.all()
