from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'worker','user', 'bed', 'plant', 'comments', 'created_at', 'completed_at', 'total_cost']
        read_only_fields = ['total_cost', 'created_at', 'user', 'worker', 'completed_at']


