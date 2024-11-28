from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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
            name="count_free_beds",
            description="Count of free beds",
            type=int,
            required=required,
        ),
        OpenApiParameter(
            name="all_beds",
            description="Count of all beds",
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
        name = serializer.validated_data['name']
        all_beds = serializer.validated_data['all_beds']
        price = serializer.validated_data['price']
        FieldService.create_field(name, all_beds, price)

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
                enum=['id', 'name', 'count_free_beds', 'all_beds', 'price'],
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

    def perform_create(self, serializer):
        field = serializer.validated_data['field']
        rented_by = serializer.validated_data.get('rented_by', None)
        response = BedService.create_bed(field, rented_by)
        if isinstance(response, Response) and response.status_code != status.HTTP_201_CREATED:
            raise ValidationError(response.data["error"])

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
        summary='Rent beds',
        description='Rent a specified number of beds from a field.',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Beds successfully rented.',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request: Not enough free beds available.',
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Field not found.',
            ),
        },
        parameters=BedParameters(required=True),
        examples=[
            OpenApiExample(
                name='Rent beds for user',
                value={
                    "field": 1,
                    "beds_count": 3
                }
            )
        ],
    )
    @action(detail=False, methods=['post'])
    def rent(self, request):
        field_id = request.data.get('field')
        beds_count = request.data.get('beds_count')
        user = request.user

        log.debug(f"Attempting to rent {beds_count} beds for user with ID={user.id} in field with ID={field_id}")

        # Получаем поле по ID
        try:
            field = Field.objects.get(id=field_id)
        except Field.DoesNotExist:
            return Response({'error': 'Field not found'}, status=status.HTTP_404_NOT_FOUND)

        rented_beds = BedService.rent_beds(field, user, beds_count)

        if rented_beds == 0:
            return Response({'error': 'Not enough free beds available for rent.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': f'{beds_count} beds rented successfully.',
            'rented_beds': [{'id': bed.id, 'position': bed.position, 'is_rented': bed.is_rented} for bed in rented_beds]
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Release beds',
        description='Release a specified number of rented beds from a field.',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Beds successfully released.',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request: Not enough rented beds.',
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Field not found.',
            ),
        },
        parameters=BedParameters(required=True),
        examples=[
            OpenApiExample(
                name='Release beds for user',
                value={
                    "field": 1,
                    "beds_count": 2
                }
            )
        ],
    )
    @action(detail=False, methods=['post'])
    def release(self, request):
        field_id = request.data.get('field')
        beds_count = request.data.get('beds_count')

        log.debug(f"Attempting to release {beds_count} beds in field with ID={field_id}")

        # Получаем поле по ID
        try:
            field = Field.objects.get(id=field_id)
        except Field.DoesNotExist:
            return Response({'error': 'Field not found'}, status=status.HTTP_404_NOT_FOUND)

        BedService.release_beds(field, beds_count)

        # Возвращаем успешный ответ
        return Response({
            'message': f'{beds_count} beds released successfully.'
        }, status=status.HTTP_200_OK)


    def get_queryset(self):
        is_rented = self.request.query_params.get('is_rented', None)
        if is_rented is not None:
            log.debug(f"Filtering beds by is_rented={is_rented}")
            return BedService.filter_beds(is_rented=is_rented.lower() == 'true')
        log.debug("Returning all beds")
        return Bed.objects.all()
