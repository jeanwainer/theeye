from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer


class EventView(viewsets.ModelViewSet):
    """
    Initial basic code
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer