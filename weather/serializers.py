from dataclasses import fields
from rest_framework import serializers

from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        exclude = ('created_at', 'updated_at')