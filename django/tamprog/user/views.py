from rest_framework import viewsets
from .permission import *
from .models import *
from .serializers import *
from rest_framework import generics, status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .services import *
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema, extend_schema_view, \
    OpenApiResponse, OpenApiParameter, OpenApiExample

User = get_user_model()

@extend_schema(tags=['User'])
class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(
        summary='Login user', 
        request=LoginSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="User logged in successfully",
                examples=[
                    OpenApiExample(
                        name="Successful login",
                        value={
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
                            "access": "eyJ0eXAi",
                            "wallet_balance": 250.00,
                        },
                    )
                ],
                response=LoginSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid credentials",
                examples=[
                    OpenApiExample(
                        name="Invalid credentials",
                        value={
                            "detail": "Invalid credentials"
                        },
                    )
                ],
                response=LoginSerializer,
            )
        },
        parameters=[
            OpenApiParameter(
                name="username",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            ),
            OpenApiParameter(
                name="password",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            )
        ],
        examples=[
            OpenApiExample(
                name="User login",
                value={
                    "username": "oleg189",
                    "password": "i_l0v3_my_cat53"
                },
                request_only=True,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'wallet_balance': user.wallet_balance,
            })
        return Response({"detail": "Invalid credentials"}, status=400)

@extend_schema(tags=['User'])
@extend_schema(methods=['PUT', 'GET', 'PATCH', 'DELETE'], exclude=True)
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (PostOnly,)

    @extend_schema(
        summary='Register new user', 
        request=LoginSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="User registered successfully",
                examples=[
                    OpenApiExample(
                        name="Successful registration",
                        value={
                            "message": "User created successfully", 
                            "user_id": 1,
                            "username": "oleg189",
                        },
                    )
                ],
                response=LoginSerializer,
            ),
        },
        parameters=[
            OpenApiParameter(
                name="username",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            ),
            OpenApiParameter(
                name="full_name",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            ),
            OpenApiParameter(
                name="phone_number",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            ),
            OpenApiParameter(
                name="password",
                location=OpenApiParameter.QUERY,
                type=str,
                description=None,
            ),
            OpenApiParameter(
                name="wallet_balance",
                location=OpenApiParameter.QUERY,
                type=float,
                description=None,
            ),
        ],
        examples=[
            OpenApiExample(
                name="Register new user",
                value={
                    "username": "oleg189",
                    "full_name": "Oleg Ivanov",
                    "phone_number": "+79991234567",
                    "password": "i_l0v3_my_cat53",
                    "wallet_balance": 250.00
                },
                request_only=True,
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Вызываем сервисную функцию для создания пользователя
        user = PersonService.create_user(
            username=serializer.validated_data['username'],
            full_name=serializer.validated_data['full_name'],
            phone_number=serializer.validated_data['phone_number'],
            password=serializer.validated_data['password'],
            wallet_balance=serializer.validated_data.get('wallet_balance', 0.00)
        )

        # Возвращаем успешный ответ с данными о пользователе
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User created successfully", "user_id": user.id, "username": user.username},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

@extend_schema(tags=['User'])
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=['User'])
class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [AgronomistPermission]

    def list(self, request, *args, **kwargs):
        ascending = request.query_params.get('asc', 'true').lower() == 'true'
        workers = WorkerService.get_sorted_workers(ascending)
        serializer = self.get_serializer(workers, many=True)
        return Response(serializer.data)