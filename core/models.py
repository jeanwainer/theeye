from django.db import models


class Event(models.Model):
    session_id = models.CharField(max_length=36, db_index=True)
    category = models.CharField(max_length=30, db_index=True)
    name = models.CharField(max_length=30)
    data = models.JSONField()
    timestamp = models.DateTimeField(db_index=True)
    saved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class ErrorLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    payload = models.TextField()
