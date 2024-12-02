from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from .serializer import *
from .models import Order
from .services import OrderService
from logging import getLogger

log = getLogger(__name__)

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
            name="comments",
            description="Comment to perform",
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
        log.debug(f"Creating order for user with ID={request.user.id}")
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
        log.debug(f"Getting all orders for user with ID={request.user.id}")
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
        log.debug(f"Getting order with ID={kwargs['pk']} for user with ID={request.user.id}")
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
        log.debug(f"Updating order with ID={kwargs['pk']} for user with ID={request.user.id}")
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
                    "comments": "water",
                    "completed_at": "2022-01-01T00:00:00Z"
                },
                request_only=True,
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        log.debug(f"Partially updating order with ID={kwargs['pk']} for user with ID={request.user.id}")
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
        log.debug(f"Deleting order with ID={kwargs['pk']} for user with ID={request.user.id}")
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        field = serializer.validated_data['field']
        plant = serializer.validated_data['plant']
        beds_count = serializer.validated_data['beds_count']
        comments = serializer.validated_data['comments']
        fertilize = serializer.validated_data.get('fertilize', False)

        log.debug(f"Creating order for user with ID={user.id}")
        response = OrderService.create_order(user, field, plant, beds_count, comments, fertilize)

        if isinstance(response, Response):
            if response.status_code == status.HTTP_201_CREATED:
                return response
            else:
                raise ValidationError(response.data.get("error", "Unknown error"))

    def perform_update(self, serializer):
        order = serializer.save()
        if order.completed_at:
            log.debug(f"Completing order with ID={order.id}")
            OrderService.complete_order(order)

    @extend_schema(
        summary='List all orders for current user',
        description='List all orders for current user',
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Successful response with list of orders',
                response=OrderSerializer(many=True),
            )
        },
    )
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        orders = OrderService.get_orders(request.user)
        serializer = self.get_serializer(orders, many=True)
        log.debug(f"Returning list of orders by user: {serializer.data}")
        return Response(serializer.data)

    def get_queryset(self):
        is_completed = self.request.query_params.get('is_completed', None)
        if is_completed is not None:
            log.debug(f"Filtering orders by is_completed={is_completed}")
            return OrderService.filter_orders(is_completed=is_completed.lower() == 'true')
        log.debug("Getting all orders")
        return Order.objects.all()
