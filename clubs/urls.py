from django.urls import path
from . import views

app_name = "clubs"

urlpatterns = [
    path("", views.club_list, name="list"),
    path("<int:pk>/", views.club_detail, name="detail"),
    #path("create/", views.create_club, name="create"),
    #path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),  # namespaced as clubs:home
    #path('dashboard/', views.president_dashboard, name='president_dashboard'),
]

