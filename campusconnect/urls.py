from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from clubs.views import home  # import the home view

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # Redirect root `/` to login page
    path('', RedirectView.as_view(pattern_name='users:login', permanent=False)),
    # After login → this is the global home (dashboard/landing)
    path('home/', home, name='home'),

    # App-specific URLs
    path("clubs/", include(("clubs.urls", "clubs"), namespace="clubs")),
    path("events/", include(("events.urls", "events"), namespace="events")),
    path("users/", include(("users.urls", "users"), namespace="users")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
