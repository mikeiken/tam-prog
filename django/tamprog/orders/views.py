from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import *
from .models import Order
from .services import OrderService

from drf_spectacular.utils import extend_schema, extend_schema_view, \
    OpenApiResponse, OpenApiParameter, OpenApiExample

@extend_schema(tags=['Order'])
@extend_schema(
    methods=['post'],
    summary='Place order',
    description='Place an order for a worker to perform an action on a bed with a plant',
    request=OrderSerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="Order created successfully",
            examples=[
                OpenApiExample(
                    name="Successful order",
                    value={},
                )
            ],
            response=OrderSerializer,
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Not enough money on the account",
            examples=[
                OpenApiExample(
                    name="Not enough money",
                    value={
                        "detail": "Top up your account"
                    },
                )
            ],
            response=OrderSerializer,
        )
    },
    parameters=[
        OpenApiParameter(
            name="worker",
            location=OpenApiParameter.QUERY,
            type=int,
            description=None,
        ),
        OpenApiParameter(
            name="user",
            location=OpenApiParameter.QUERY,
            type=int,
            description=None,
        ),
        OpenApiParameter(
            name="bed",
            location=OpenApiParameter.QUERY,
            type=int,
            description=None,
        ),
        OpenApiParameter(
            name="plant",
            location=OpenApiParameter.QUERY,
            type=int,
            description=None,
        ),
        OpenApiParameter(
            name="action",
            location=OpenApiParameter.QUERY,
            type=str,
            description=None,
        ),
        OpenApiParameter(
            name="completed_at",
            location=OpenApiParameter.QUERY,
            type=str,
            description=None,
        ),
    ],
    examples=[
        OpenApiExample(
            name="Place order",
            value={
                "worker": 1,
                "user": 1,
                "bed": 1,
                "plant": 1,
                "action": "water",
                "completed_at": "2022-01-01T00:00:00Z"
            },
            request_only=True,
        ),
    ]
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get all orders',
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Orders retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Successful orders",
                        # TODO: OrderViewSet: write response example
                        value={},
                    )
                ],
                response=OrderSerializer,
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
                examples=[
                    OpenApiExample(
                        name="Successful order",
                        # TODO: OrderViewSet: write response example
                        value={},
                    )
                ],
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
                examples=[
                    OpenApiExample(
                        name="Successful update",
                        # TODO: OrderViewSet: write response example
                        value={},
                    )
                ],
                response=OrderSerializer,
            ),
        },
        parameters=[
            OpenApiParameter(
                name="worker",
                location=OpenApiParameter.QUERY,
                type=int,
                description=None,
            ),
            OpenApiParameter(
                name="user",
                location=OpenApiParameter.QUERY,
                type=int,
                description=None,
            ),
            OpenApiParameter(
                name="bed",
                location=OpenApiParameter.QUERY,
                type=int,
                description=None,
            ),
            OpenApiParameter(
                name="plant",
                location=OpenApiParameter.QUERY,
                type=int,
                description=None,
            ),
            OpenApiParameter(
                name="action",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            ),
            OpenApiParameter(
                name="completed_at",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            ),
        ],
        examples=[
            OpenApiExample(
                name="Update order",
                value={
                    "worker": 1,
                    "user": 1,
                    "bed": 1,
                    "plant": 1,
                    "action": "water",
                    "completed_at": "2022-01-01T00:00:00Z"
                },
                request_only=True,
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary='Partial update order',
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Order updated successfully",
                examples=[
                    OpenApiExample(
                        name="Successful update",
                        # TODO: OrderViewSet: write response example
                        value={},
                    )
                ],
                response=OrderSerializer,
            ),
        },
        parameters=[
            OpenApiParameter(
                name="worker",
                location=OpenApiParameter.QUERY,
                type=int,
                description=None,
            ),
            OpenApiParameter(
                name="user",
                location=OpenApiParameter.QUERY,
                type=int,
                description=None,
            ),
            OpenApiParameter(
                name="bed",
                location=OpenApiParameter.QUERY,
                type=int,
                description=None,
            ),
            OpenApiParameter(
                name="plant",
                location=OpenApiParameter.QUERY,
                type=int,
                description=None,
            ),
            OpenApiParameter(
                name="action",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            ),
            OpenApiParameter(
                name="completed_at",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            ),
        ],
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
                    "worker": 1,
                    "user": 1,
                    "bed": 1,
                    "plant": 1,
                    "action": "water",
                    "completed_at": "2022-01-01T00:00:00Z"
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Change worker",
                value={
                    "worker": 56
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
            # TODO: OrderViewSet: write response codes
            
            # TODO: OrderViewSet: write response example
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

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

    def get_queryset(self):
        is_completed = self.request.query_params.get('is_completed', None)
        if is_completed is not None:
            return OrderService.filter_orders(is_completed=is_completed.lower() == 'true')
        return Order.objects.all()
