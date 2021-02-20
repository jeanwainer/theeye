import json

from celery import shared_task

from .serializers import EventSerializer
from .models import ErrorLog


@shared_task
def process_event(data):
    serializer = EventSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        errors = []
        for k,v in serializer.errors.items():
            errors.append(f'{k}: {",".join(v)}')

        ErrorLog.objects.create(payload=json.dumps(data), error=','.join(errors))

