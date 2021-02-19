from datetime import datetime
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer
from .tasks import process_event


class EventView(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def create(self, request, *args, **kwargs):
        process_event.delay(request.data)
        # Celery task will be called from here
        return Response(status=status.HTTP_202_ACCEPTED)

    def get_queryset(self):
        """
        Customize method to filter by parameters
        """
        queryset = Event.objects.all()

        start_date = self.request.query_params.get('start_date')
        if start_date:
            start_date = datetime.fromisoformat(start_date)
            queryset = queryset.filter(timestamp__gte=start_date)

        end_date = self.request.query_params.get('end_date')
        if end_date:
            end_date = datetime.fromisoformat(end_date)
            queryset = queryset.filter(timestamp__lte=end_date)

        end_date = self.request.query_params.get('end_date')
        if end_date:
            end_date = datetime.fromisoformat(end_date)
            queryset = queryset.filter(timestamp__lte=end_date)

        session_id = self.request.query_params.get('session_id')
        if session_id:
            queryset = queryset.filter(session_id=session_id)

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset
