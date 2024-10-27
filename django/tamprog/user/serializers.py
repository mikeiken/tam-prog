from rest_framework import serializers
from .models import Person, Agronomist, Worker


from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'wallet_balance', 'full_name', 'phone_number']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'full_name', 'phone_number', 'password', 'wallet_balance')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with this phone number already exists.")
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class AgronomistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agronomist
        fields = ['id', 'name']

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'name']
