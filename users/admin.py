from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # ✅ update what fields are shown in the admin list
    list_display = ("email", "full_name", "college_id", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "department")

    # ✅ set ordering to email instead of username
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password", "full_name", "college_id", "department", "section", "phone_number", "dayscholar")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "college_id", "department", "section", "phone_number", "dayscholar", "password1", "password2", "is_staff", "is_active"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
