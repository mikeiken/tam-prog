from rest_framework import serializers
from .models import Field, Bed

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'

class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ['id', 'field', 'is_rented', 'rented_by']
        read_only_fields = ['is_rented', 'rented_by']
