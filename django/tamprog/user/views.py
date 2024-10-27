from rest_framework import viewsets
from .permissions import PostOnly
from .models import *
from .serializers import *
from rest_framework import generics, status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .services import PersonService
from django.contrib.auth import get_user_model
User = get_user_model()
class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

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


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (PostOnly,)

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
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class AgronomistViewSet(viewsets.ModelViewSet):
    queryset = Agronomist.objects.all()
    serializer_class = AgronomistSerializer

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer