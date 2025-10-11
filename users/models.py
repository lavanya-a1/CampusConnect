from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None   # 🔴 remove username completely
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=100, blank=True)
    college_id = models.CharField(max_length=50, blank=True)
    department_choices = [
        ("CSE", "CSE"),
        ("IT", "IT"),
        ("CSE-AIDS", "CSE-AIDS"),
        ("CSE-AIML", "CSE-AIML"),
        ("CSE-CS", "CSE-CS"),
        ("ECE", "ECE"),
        ("EEE", "EEE"),
        ("MECH", "MECH"),
        ("CIVIL", "CIVIL"),
    ]
    department = models.CharField(max_length=20, choices=department_choices, blank=True)
    section = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    dayscholar = models.BooleanField(default=False)

    USERNAME_FIELD = "email"         # 🔑 login with email
    REQUIRED_FIELDS = []             # nothing else required for superuser

    objects = CustomUserManager()    # use custom manager

    def __str__(self):
        return self.email
