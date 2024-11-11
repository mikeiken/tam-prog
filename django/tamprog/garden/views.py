from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .permission import *
from .models import Field, Bed
from .serializers import FieldSerializer, BedSerializer
from .services import *

from drf_spectacular.utils import extend_schema, extend_schema_view, \
    OpenApiResponse, OpenApiParameter, OpenApiExample

@extend_schema(tags=['Field'])
class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [AgronomistPermission]

    # put
    def perform_create(self, serializer):
        count_beds = self.request.data.get('count_beds', 0)
        serializer.save(count_beds=count_beds)

    # sort
    def list(self, request, *args, **kwargs):
        sort_by = request.query_params.get('sort', 'price')
        ascending = request.query_params.get('asc', 'true').lower() == 'true'
        fields = FieldService.get_sorted_fields(sort_by, ascending)
        serializer = self.get_serializer(fields, many=True)
        return Response(serializer.data)
    


@extend_schema(tags=['Bed'])
@extend_schema(
    methods=['post'],
    summary='Create bed',
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description='Successful response with created bed',
            response=BedSerializer,
        ),
    }
)
class BedViewSet(viewsets.ModelViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List all beds',
        description='List all beds',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with list of beds',
                examples=[
                    OpenApiExample(
                        name='List of beds',
                        value=[
                            {
                                "id": 1,
                                "is_rented": True,
                                "field": 1,
                                "rented_by": 1
                            },
                            {
                                "id": 2,
                                "is_rented": True,
                                "field": 2,
                                "rented_by": 1
                            }
                        ]
                    )
                ],
                response=BedSerializer,
            )
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary='Retrieve bed',
        description='Retrieve bed by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with bed',
                examples=[
                    OpenApiExample(
                        name='Bed',
                        value={
                            "id": 1,
                            "is_rented": True,
                            "field": 1,
                            "rented_by": 1
                        }
                    )
                ],
                response=BedSerializer,
            )
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update bed',
        description='Update bed by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with updated bed',
                examples=[
                    OpenApiExample(
                        name='Updated bed',
                        value={
                            "id": 1,
                            "is_rented": True,
                            "field": 1,
                            "rented_by": 1
                        }
                    )
                ],
                response=BedSerializer,
            )
        },
        parameters=[
            OpenApiParameter(
                name='is_rented',
                type=bool,
                description='Is bed rented',
                required=True,
            ),
            OpenApiParameter(
                name='field',
                type=int,
                description='Field ID',
                required=True,
            ),
            OpenApiParameter(
                name='rented_by',
                type=int,
                description='User ID',
                required=True,
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
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
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary='Partial update bed',
        description='Partial update bed by ID',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with updated bed',
                examples=[
                    OpenApiExample(
                        name='Updated bed',
                        value={
                            "id": 1,
                            "is_rented": True,
                            "field": 1,
                            "rented_by": 1
                        }
                    )
                ],
                response=BedSerializer,
            )
        },
        parameters=[
            OpenApiParameter(
                name='is_rented',
                type=bool,
                description='Is bed rented',
                required=True,
            ),
            OpenApiParameter(
                name='field',
                type=int,
                description='Field ID',
                required=True,
            ),
            OpenApiParameter(
                name='rented_by',
                type=int,
                description='User ID',
                required=True,
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='List all beds for current user',
        description='List all beds that are rented by the current user',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with list of beds',
                examples=[
                    OpenApiExample(
                        name='List of beds for user',
                        value=[
                            {
                                "id": 1,
                                "is_rented": True,
                                "field": 1,
                                "rented_by": 1
                            },
                            {
                                "id": 2,
                                "is_rented": True,
                                "field": 2,
                                "rented_by": 1
                            }
                        ]
                    )
                ],
                response=BedSerializer,
            )
        },
    )
    @action(detail=False, methods=['get'])
    def my_beds(self, request):
        beds = BedService.get_user_beds(request.user)
        serializer = self.get_serializer(beds, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Rent bed',
        description='Rent bed for',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request',
            ),
        },
        parameters=[
            OpenApiParameter(
                name='is_rented',
                type=bool,
                description='Is bed rented',
                required=True,
            ),
            OpenApiParameter(
                name='field',
                type=int,
                description='Field ID',
                required=True,
            ),
            OpenApiParameter(
                name='rented_by',
                type=int,
                description='User ID',
                required=True,
            ),
        ],
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
        result = BedService.rent_bed(bed.id, person)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Release bed',
        description='Release bed',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Bad request',
            ),
        },
        parameters=[
            OpenApiParameter(
                name='is_rented',
                type=bool,
                description='Is bed rented',
                required=True,
            ),
            OpenApiParameter(
                name='field',
                type=int,
                description='Field ID',
                required=True,
            ),
            OpenApiParameter(
                name='rented_by',
                type=int,
                description='User ID',
                required=True,
            ),
        ],
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
        result = BedService.release_bed(bed.id)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        is_rented = self.request.query_params.get('is_rented', None)
        if is_rented is not None:
            return BedService.filter_beds(is_rented=is_rented.lower() == 'true')
        return Bed.objects.all()
