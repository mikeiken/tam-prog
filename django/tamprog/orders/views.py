from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import *
from .models import Order
from .services import OrderService

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        worker = serializer.validated_data['worker']
        bed = serializer.validated_data['bed']
        plant = serializer.validated_data['plant']
        action = serializer.validated_data['action']
        order = OrderService.create_order(user, worker, bed, plant, action)
        if order:
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Top up your account'}, status=status.HTTP_400_BAD_REQUEST)


    def perform_update(self, serializer):
        order = serializer.save()
        if order.completed_at:
            OrderService.complete_order(order)
