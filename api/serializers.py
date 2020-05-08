from rest_framework import serializers
from .models import APItest


class APItestSerializer(serializers.ModelSerializer):
    class Meta:
        model = APItest
        fields = ('id', 'name', 'email', 'message')
