from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=200)
    lyrics = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="songs", default=0)


    def __str__(self):
        return f"{self.title} - {self.created_at}"
    