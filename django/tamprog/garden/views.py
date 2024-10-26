from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Field, Bed
from .serializers import FieldSerializer, BedSerializer
from .services import create_field, rent_bed, release_bed, get_user_beds

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        count_beds = self.request.data.get('count_beds', 0)  # Получаем количество грядок из запроса
        serializer.save(count_beds=count_beds)



class BedViewSet(viewsets.ModelViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def my_beds(self, request):
        beds = get_user_beds(request.user)
        serializer = self.get_serializer(beds, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rent(self, request, pk=None):
        field = Field.objects.get(id=pk)
        bed = rent_bed(field, request.user)
        return Response({'bed_id': bed.id})

    @action(detail=True, methods=['post'])
    def release(self, request, pk=None):
        bed = self.get_object()
        release_bed(bed)
        return Response({'status': 'bed released'})
