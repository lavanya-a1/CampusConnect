from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="list"),
    path("<int:pk>/", views.event_detail, name="detail"),
    path("create/", views.create_event, name="create"),
    path('<int:event_id>/register/', views.register, name='register'),
    path("<int:pk>/upload/", views.upload_gallery, name="upload_gallery"),
    path('dashboard/', views.president_dashboard, name='president_dashboard'),

]