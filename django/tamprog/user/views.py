from rest_framework import viewsets
from .models import Person, Agronomist, Worker
from .serializers import PersonSerializer, AgronomistSerializer, WorkerSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class AgronomistViewSet(viewsets.ModelViewSet):
    queryset = Agronomist.objects.all()
    serializer_class = AgronomistSerializer

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
