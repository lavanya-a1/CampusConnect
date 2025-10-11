
# Create your models here.
from django.db import models
from django.conf import settings


class Club(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="club_logos/", blank=True, null=True)
    description = models.TextField()
    faculty_coordinator = models.CharField(max_length=100)

    # New fields
    faculty_coordinator_number = models.CharField(max_length=15, blank=True, null=True)
    president_name = models.CharField(max_length=100, blank=True, null=True)
    president_contact = models.CharField(max_length=15, blank=True, null=True)
    vice_president_name = models.CharField(max_length=100, blank=True, null=True)
    secretary_name = models.CharField(max_length=100, blank=True, null=True)
    treasurer_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Member(models.Model):
    ROLE_CHOICES = (("lead", "Lead"), ("member", "Member"))
    club = models.ForeignKey(Club, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    def __str__(self):
        return f"{self.user.username} — {self.club.name}"

