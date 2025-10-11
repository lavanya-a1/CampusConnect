# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Registration, EventGallery
from .forms import EventForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from clubs.models import Member,Club

def event_list(request):
    upcoming_events = Event.objects.filter(completed=False).order_by("date")
    completed_events = Event.objects.filter(completed=True).order_by("-date")
    
    # Check if user can create events (admin/staff or president of any club)
    can_create_events = False
    if request.user.is_authenticated:
        can_create_events = (
            request.user.is_superuser or 
            request.user.is_staff or 
            Member.objects.filter(user=request.user, role="lead").exists()
        )
    
    return render(request, "events/event_list.html", {
        "upcoming_events": upcoming_events, 
        "completed_events": completed_events,
        "can_create_events": can_create_events
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "events/event_detail.html", {"event": event})


@login_required
def create_event(request):
    # Leads (presidents) can create events for their clubs
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            # Verify the user is a lead for the selected club
            is_lead = Member.objects.filter(club=event.club, user=request.user, role="lead").exists()
            if not (request.user.is_superuser or request.user.is_staff or is_lead):
                raise PermissionDenied("You are not authorized to create events for this club.")
            event.save()
            return redirect("events:detail", pk=event.pk)
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form})
# events/views.py


@login_required
def register(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registered = False
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create registration for this user and event
            Registration.objects.get_or_create(event=event, user=request.user)
            registered = True
            # Send confirmation email
            send_mail(
                subject=f"Registration Confirmed: {event.title}",
                message=f"You have successfully registered for {event.title} on {event.date.strftime('%b %d, %Y %H:%M')} at {event.venue}.\n\nEvent Details:\n{event.description}",
                from_email=None,  # uses DEFAULT_FROM_EMAIL
                recipient_list=[request.user.email],
                fail_silently=False,  # Show errors if email fails
            )
    else:
        form = RegistrationForm()
    return render(request, 'events/register.html', {'event': event, 'form': form, 'registered': registered})



@login_required
def upload_gallery(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.completed:
        raise PermissionDenied("Gallery uploads are allowed only for completed events.")
    if request.method == "POST" and request.FILES.get("image"):
        EventGallery.objects.create(event=event, image=request.FILES["image"])
        return redirect("events:detail", pk=pk)
    return render(request, "events/upload_gallery.html", {"event": event})



@login_required
def president_dashboard(request):
    # Clubs where the user is a lead (president)
    lead_clubs = Club.objects.filter(members__user=request.user, members__role="lead").distinct()

    clubs_with_events = []
    for club in lead_clubs:
        upcoming = club.events.filter(completed=False).order_by("date")
        completed = club.events.filter(completed=True).order_by("-date")
        clubs_with_events.append({
            "club": club,
            "upcoming_events": upcoming,
            "completed_events": completed,
        })

    return render(request, "events/president_dashboard.html", {"clubs_with_events": clubs_with_events})
