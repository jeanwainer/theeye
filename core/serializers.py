from django.utils import timezone
from rest_framework import serializers

from .models import Event, ErrorLog


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['saved_date',]

    def validate_data(self, value):
        """
        Validates if payload is not empty and is a valid dictionary
        """
        if value == '':
            raise serializers.ValidationError("Payload is empty")
        try:
            dict(value)
        except ValueError:
            raise serializers.ValidationError("Payload is not valid")

        return value

    def validate_timestamp(self, value):
        """
        Validate whether timestamp is a valid date (not greater than current date)
        """
        if value > timezone.now():
            raise serializers.ValidationError("Timestamp is invalid")

        return value


class ErrorLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ErrorLog
        fields = '__all__'