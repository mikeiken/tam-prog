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

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [AgronomistPermission]

    # post
    @extend_schema(
        summary='Post', 
    )
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
    



class BedViewSet(viewsets.ModelViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_beds(self, request):
        beds = BedService.get_user_beds(request.user)
        serializer = self.get_serializer(beds, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rent(self, request, pk=None):
        bed = self.get_object()
        person = request.user
        result = BedService.rent_bed(bed.id, person)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
