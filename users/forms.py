from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# Signup form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["full_name", "college_id", "email", "department", "section", "phone_number", "dayscholar"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "college_id": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-select"}),
            "section": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "dayscholar": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        import re
        
        # Check if email ends with the correct domain
        if not email.endswith("@svecw.edu.in"):
            raise forms.ValidationError("You must use your college email (…@svecw.edu.in)")
        
        # Extract the local part (before @)
        local_part = email.split("@")[0]
        
        # Check for the specific pattern: XXboXXXXXX@svecw.edu.in
        # Where XX can be any 2 characters and XXXXXX can be any 6 characters
        pattern = r'^[0-9]{2}b0[A-Za-z0-9]{6}$'
        
        if not re.match(pattern, local_part):
            raise forms.ValidationError(
                "Email must follow the college format: XXb0XXXXXX@svecw.edu.in "
            )
        
        return email


# Edit profile form
class CustomUserChangeForm(UserChangeForm):
    password = None  # hide password field

    class Meta:
        model = CustomUser
        fields = ["full_name", "college_id", "email", "department", "section", "phone_number", "dayscholar"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "college_id": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-select"}),
            "section": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "dayscholar": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        import re
        
        # Check if email ends with the correct domain
        if not email.endswith("@svecw.edu.in"):
            raise forms.ValidationError("You must use your college email (…@svecw.edu.in)")
        
        # Extract the local part (before @)
        local_part = email.split("@")[0]
        
        # Check for the specific pattern: XXboXXXXXX@svecw.edu.in
        # Where XX can be any 2 characters and XXXXXX can be any 6 characters
        pattern = r'^[A-Za-z0-9]{2}bo[A-Za-z0-9]{6}$'
        
        if not re.match(pattern, local_part):
            raise forms.ValidationError(
                "Email must follow the college format: XXb0XXXXXX@svecw.edu.in "
            )
        
        return email
