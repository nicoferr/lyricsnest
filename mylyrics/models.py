from django.db import models
from django.utils import timezone

class Song(models.Model):
    title = models.CharField(max_length=200)
    lyrics = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.title} - {self.created_at}"
    