from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .permission import *
from .models import Field, Bed
from .serializers import FieldSerializer, BedSerializer
from .services import BedService


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [AgronomistPermission]

    def perform_create(self, serializer):
        count_beds = self.request.data.get('count_beds', 0)
        serializer.save(count_beds=count_beds)


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
