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

def LoginParameters(required=False):
    return [
        OpenApiParameter(
            name="username",
            description="Username",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="password",
            description="Password",
            type=str,
            required=required,
        ),
    ]

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
                            "refresh": "string",
                            "access": "string",
                            "wallet_balance": 0.00,
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
        parameters=LoginParameters(required=True),
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

def RegisterParameters(required=False):
    return [
        OpenApiParameter(
            name="username",
            description="Username",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="full_name",
            description="Full name",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="phone_number",
            description="Phone number",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="password",
            description="Password",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="wallet_balance",
            description="Wallet balance",
            type=float,
        ),
    ]

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
                            "user_id": 0,
                            "username": "string",
                        },
                    )
                ],
                response=LoginSerializer,
            ),
        },
        parameters=RegisterParameters(required=True),
        examples=[
            OpenApiExample(
                name="Register new user",
                value={
                    "username": "string",
                    "full_name": "string",
                    "phone_number": "string",
                    "password": "string",
                    "wallet_balance": 0.00
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

def PersonParameters(required=False):
    return [
        OpenApiParameter(
            name="wallet_balance",
            description="User wallet balance",
            type=float,
            required=required,
        ),
        OpenApiParameter(
            name="full_name",
            description="User full name",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="phone_number",
            description="User phone number",
            type=str,
            required=required,
        ),
    ]

@extend_schema(tags=['User'])
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary='Get all users', 
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Successful response",
                response=PersonSerializer(many=True),
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary='Get user by ID', 
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Successful response",
                response=PersonSerializer,
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update user', 
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="User updated successfully",
            ),
        },
        parameters=PersonParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Partial update user', 
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="User updated successfully",
            ),
        },
        parameters=PersonParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Delete user', 
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="User deleted successfully",
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

def WorkerParameters(required=False):
    return [
        OpenApiParameter(
            name="name",
            description="Worker full name",
            type=str,
            required=required,
        ),
        OpenApiParameter(
            name="price",
            description="Worker salary",
            type=float,
            required=required,
        ),
        OpenApiParameter(
            name="description",
            description="Worker description",
            type=str,
            required=required,
        ),
    ]

@extend_schema(tags=['User'])
class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [AgronomistPermission]

    @extend_schema(
        summary='Get all workers', 
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Successful response",
                response=WorkerSerializer(many=True),
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        ascending = request.query_params.get('asc', 'true').lower() == 'true'
        workers = WorkerService.get_sorted_workers.delay(ascending)
        serializer = self.get_serializer(workers, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary='Get worker by ID', 
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Successful response",
                response=WorkerSerializer,
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update worker', 
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Worker updated successfully",
            ),
        },
        parameters=WorkerParameters(required=True),
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary='Update worker', 
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Worker updated successfully",
            ),
        },
        parameters=WorkerParameters(required=True),
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Partial update worker', 
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Worker updated successfully",
            ),
        },
        parameters=WorkerParameters(),
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary='Delete worker', 
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Worker deleted successfully",
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    