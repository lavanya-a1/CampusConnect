from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})

@login_required
def profile(request):
    return render(request, "users/profile.html")

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})
from django.contrib.auth import views as auth_views


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})