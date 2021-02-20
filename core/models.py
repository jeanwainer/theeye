from django.db import models


class Event(models.Model):
    session_id = models.CharField(max_length=36)
    category = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    data = models.JSONField()
    timestamp = models.DateTimeField()
    saved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class ErrorLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    payload = models.TextField()
    error = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.created.isoformat()

