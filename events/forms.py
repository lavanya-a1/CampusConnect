from django import forms
from .models import Event, Registration

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["club", "title", "description", "date", "venue", "completed"]
        widgets = {"date": forms.DateTimeInput(attrs={"type":"datetime-local"})}

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = []  # No extra fields, just event and user 