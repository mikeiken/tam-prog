from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order
from orders.serializer import OrderSerializer
from .services import create_order, complete_order

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        worker = serializer.validated_data['worker']
        bed = serializer.validated_data['bed']
        plant = serializer.validated_data['plant']
        action = serializer.validated_data['action']
        create_order(self.request.user, worker, bed, plant, action)


    def perform_update(self, serializer):
        order = serializer.save()
        if order.completed_at:
            complete_order(order)

