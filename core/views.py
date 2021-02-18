from datetime import datetime
from rest_framework import viewsets, mixins
from .models import Event
from .serializers import EventSerializer


class EventView(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    Initial basic code
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

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

        session = self.request.query_params.get('session')
        if session:
            queryset = queryset.filter(session=session)

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset
