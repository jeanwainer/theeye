from datetime import datetime
from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['saved_date',]

    def validate_timestamp(self, value):
        """
        Validate whether timestamp is a valid date (not greater than current date)
        """
        if value > datetime.now():
            raise serializers.ValidationError("Timestamp is invalid")

        return value
