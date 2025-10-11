from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Club, Member
from .forms import ClubForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from events.models import Event

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log user in after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})


def club_list(request):
    clubs = Club.objects.all()
    return render(request, "clubs/club_list.html", {"clubs": clubs})

def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    return render(request, "clubs/club_detail.html", {"club": club})


from django.core.exceptions import PermissionDenied

@login_required
def create_club(request):
    # Only allow superusers or staff (club admins) to create clubs
    if not request.user.is_superuser and not request.user.is_staff:
        raise PermissionDenied("Only club admins or superusers can add clubs.")
    if request.method == "POST":
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("clubs:club_list")
    else:
        form = ClubForm()
    return render(request, "clubs/club_form.html", {"form": form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    return render(request, "home.html")
