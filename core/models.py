from django.db import models


class Event(models.Model):
    session_id = models.CharField(max_length=36)
    category = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    data = models.JSONField()
    timestamp = models.DateTimeField()
    saved_date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ['-timestamp']
