# users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'wallet_balance', 'phone_number', 'account_number', 'full_name']
        read_only_fields = ['username']

    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        return value

    def validate_account_number(self, value):
        if not value:
            raise serializers.ValidationError("Account number is required.")
        return value

    def validate_full_name(self, value):
        if not value:
            raise serializers.ValidationError("Full name is required.")
        return value
