from django.shortcuts import render, redirect
from event.models import Event
from datetime import date

# Create your views here.


def home(request):
    events = Event.objects.select_related("category").prefetch_related("participants")
    today = date.today()
    up_events = events.filter(date__gte=today)
    context = {
        "up_events": up_events,
    }
    return render(request,"home.html",context)

def no_permission(request):
    return render(request,"no_permission.html")


def redirect_to_dashboard(request):
    if request.user.groups.filter(name="Organizer").exists():
        print("printing from core........")
        return redirect("dashboard")
    elif request.user.groups.filter(name="Admin").exists():
        return redirect("admin-dashboard")
    else:
        return redirect("user-dashboard")
    
    
def dummy_page(request):
    return render(request,'dummy.html',{})
    