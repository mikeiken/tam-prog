from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from fuzzywuzzy import fuzz
from rest_framework.decorators import action


from .models import *
from .serializers import *

methods = ['get', 'post', 'head',
           'put', 'patch', 'delete', 'update', 'destroy']

class CORSMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response


class AgronomistViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = Agronomist.objects.all()
    serializer_class = AgronomistSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()


class SupplierViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()


class WorkerViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()


class GardenBedViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = GardenBed.objects.all()
    serializer_class = GardenBedSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()


class FertilizerViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()


class UserViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()


class PlantViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()
    
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.GET.get('query', '')
        threshold = 70 
        
        if query:
            plants = Plant.objects.all()
            filtered_plants = []
            
            for plant in plants:
                similarity = fuzz.ratio(query.lower(), plant.name.lower())
                if similarity >= threshold:
                    filtered_plants.append((plant, similarity))
            
            filtered_plants.sort(key=lambda x: x[1], reverse=True)
            filtered_plants = [plant[0] for plant in filtered_plants]
        else:
            filtered_plants = []

        serializer = self.get_serializer(filtered_plants, many=True)
        return Response(serializer.data)


class PlotViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()


class OrderViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()

class AvailablePlantsViewSet(CORSMixin, viewsets.ModelViewSet):
    queryset = AvailablePlants.objects.all()
    serializer_class = AvailablePlantsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()
