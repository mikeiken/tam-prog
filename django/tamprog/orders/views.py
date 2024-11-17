from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import *
from .models import Order
from .services import OrderService

from drf_spectacular.utils import extend_schema, extend_schema_view, \
    OpenApiResponse, OpenApiParameter, OpenApiExample

def OrderParameters(required=False):
    return [
        OpenApiParameter(
            name="bed",
            description="Bed ID",
            type=int,
            required=required,
        ),
        OpenApiParameter(
            name="plant",
            description="Plant ID",
            type=int,
            required=required,
        ),
        OpenApiParameter(
            name="action",
            description="Action to perform",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="completed_at",
            description="Completion time",
            type=str,
            required=required,
        ),
    ]

@extend_schema(tags=['Order'])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Place order',
        description='Place an order for a worker to perform an action on a bed with a plant',
        request=OrderSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Order created successfully",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Not enough money on the account",
            )
        },
        parameters=OrderParameters(required=True),
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Get all orders',
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Orders retrieved successfully",
                response=OrderSerializer(many=True),
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary='Get order by id',
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Order retrieved successfully",
                response=OrderSerializer,
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update order',
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Order updated successfully",
            ),
        },
        parameters=OrderParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary='Partial update order',
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Order updated successfully",
            ),
        },
        parameters=OrderParameters(),
        examples=[
            OpenApiExample(
                name="Update completion time",
                value={
                    "completed_at": "2022-01-01T00:00:00Z"
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Full update order",
                description="Update all fields. Prefferebly use PUT method for this operation",
                value={
                    "bed": 1,
                    "plant": 1,
                    "action": "water",
                    "completed_at": "2022-01-01T00:00:00Z"
                },
                request_only=True,
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Delete order',
        request=OrderSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Order deleted successfully",
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        bed = serializer.validated_data['bed']
        plant = serializer.validated_data['plant']
        action = serializer.validated_data['action']
        order = OrderService.create_order(user, bed, plant, action)
        if order:
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Top up your account'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        order = serializer.save()
        if order.completed_at:
            OrderService.complete_order(order)

    def get_queryset(self):
        is_completed = self.request.query_params.get('is_completed', None)
        if is_completed is not None:
            return OrderService.filter_orders(is_completed=is_completed.lower() == 'true')
        return Order.objects.all()
