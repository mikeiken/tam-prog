from rest_framework import serializers
from .models import Field, Bed

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'name', 'count_free_beds', 'all_beds', 'price', 'url']
        read_only_fields = ['count_free_beds']

class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ['id', 'field', 'is_rented', 'rented_by']
        read_only_fields = ['is_rented', 'rented_by']
