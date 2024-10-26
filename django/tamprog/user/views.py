from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Person, Agronomist
from .serializers import UserSerializer, AgronomistSerializer
from .services import create_user, get_tokens_for_user, update_user
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', '')
        account_number = request.data.get('account_number', '')
        full_name = request.data.get('full_name', '')
        role = request.data.get('role', 'person')
        tokens = get_tokens_for_user(Person)
        return Response(tokens)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        phone_number = request.data.get('phone_number')
        account_number = request.data.get('account_number')
        full_name = request.data.get('full_name')
        update_user(user, phone_number=phone_number, account_number=account_number, full_name=full_name)
        return super().update(request, *args, **kwargs)
