from django.shortcuts import render,redirect
from django.http import HttpResponse
from event.forms import EventModelForm,CategoryModelForm,ParticipantModelForm
from django.contrib import messages
from event.models import Event, Category, Participant
from datetime import date
from django.db.models import Count

# Create your views here.

def home(request):
    return HttpResponse("Hello World!")


def check(request):
    return HttpResponse("from event")

def dashboard(request):
    type = request.GET.get('type','all')
    search = request.GET.get('q', '')
    print(type)
    
    
    events = Event.objects.select_related("category").prefetch_related("participants").annotate(participant_count=Count('participants'))
    today = date.today()
    participants = Participant.objects.all()
    up_events = events.filter(date__gte=today)
    past_events = events.filter(date__lt=today)
    
    base_query = Event.objects.select_related("category").prefetch_related("participants").annotate(participant_count=Count('participants'))
    
    if type == 'upcoming':
        events = base_query.filter(date__gte=today)
    elif type == 'past':
        events = base_query.filter(date__lt=today)
    else:
        events.all()
        
    if search:
        events = events.filter(name__icontains=search)
    context = {
        "events":events,
        "participants":participants,
        "up_events": up_events,
        "past_events":past_events,
    }
    return render(request,"dashboard.html",context)


def book_now(request):
    return render(request,"book_now.html")


def navbar(request):
    return render(request,"navbar.html")


def create_event(request):
    form = EventModelForm()
    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect("create_event")

    
    context = {
        "form" : form,
    }
    
    return render(request,"user-input/event-form.html", context)


def add_category(request):
    form = CategoryModelForm()
    if request.method == "POST":
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Category added successfully!")
            return redirect("add_category")
        
    context = {
        "form" : form,
    }
    
    return render(request,"user-input/category-form.html",context)



def add_participant(request):
    form = ParticipantModelForm()
    if request.method == "POST":
        form = ParticipantModelForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request,"Participant added successfully!")
            return redirect("add_participant")
        
    context = {
        "form": form
    }
    
    return render(request,"user-input/participants-form.html",context)





def update_event(request,id):
    event = Event.objects.get(id=id)
    form = EventModelForm(instance=event)
    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect("create_event")

    
    context = {
        "form" : form,
    }
    
    return render(request,"user-input/event-form.html", context)



def delete_event(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request,"Event Deleted succesfully!")
        Participant.objects.annotate(event_count=Count('events')).filter(event_count=0).delete()
        return redirect("dashboard")
    
    else:
        messages.error(request,"something went wrong!")
        return redirect("dashboard")
            
    