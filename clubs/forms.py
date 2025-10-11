from django import forms
from .models import Club

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = [
            "name",
            "logo",
            "description",
            "faculty_coordinator",
            "faculty_coordinator_number",
            "president_name",
            "president_contact",
            "vice_president_name",
            "secretary_name",
            "treasurer_name",
        ]
