from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from clubs.models import Club

class Event(models.Model):
    club = models.ForeignKey(Club, related_name="events", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200, blank=True)
    completed = models.BooleanField(default=False)
    calendar_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.club.name})"

class Registration(models.Model):
    event = models.ForeignKey(Event, related_name="registrations", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"

class EventGallery(models.Model):
    event = models.ForeignKey(Event, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="event_gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
