from django.contrib import admin

# Register your models here.
from .models import Event, Registration, EventGallery

admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(EventGallery)