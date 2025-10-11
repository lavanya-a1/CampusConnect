from django.contrib import admin
from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Club, Member


class ClubAdminForm(forms.ModelForm):
    lead_email = forms.EmailField(required=False, help_text="Email of the club lead (president) with site account")

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill with current lead's email if present
        if self.instance and self.instance.pk:
            lead_member = Member.objects.filter(club=self.instance, role="lead").select_related("user").first()
            if lead_member and lead_member.user and lead_member.user.email:
                self.fields["lead_email"].initial = lead_member.user.email


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    form = ClubAdminForm
    list_display = ("name", "faculty_coordinator", "current_lead_email")

    def current_lead_email(self, obj):
        lead_member = Member.objects.filter(club=obj, role="lead").select_related("user").first()
        return lead_member.user.email if lead_member and lead_member.user else "—"
    current_lead_email.short_description = "Lead Email"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        lead_email = form.cleaned_data.get("lead_email")
        if lead_email is None:
            return
        User = get_user_model()
        try:
            user = User.objects.get(email__iexact=lead_email)
        except User.DoesNotExist:
            messages.warning(request, f"Lead not set: No user account found with email {lead_email}.")
            return
        # Ensure exactly one lead mapping for this club
        Member.objects.filter(club=obj, role="lead").exclude(user=user).delete()
        Member.objects.update_or_create(
            club=obj,
            user=user,
            defaults={"role": "lead"},
        )
        messages.success(request, f"Lead updated for {obj.name} → {user.email}")


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("club", "user", "role")
    list_filter = ("role", "club")
    search_fields = ("user__email", "user__username", "club__name")