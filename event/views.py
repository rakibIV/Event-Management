from django.shortcuts import render,redirect
from django.http import HttpResponse
from event.forms import EventModelForm,CategoryModelForm
from django.contrib import messages
from event.models import Event, Category
from datetime import date
from django.db.models import Count

# Create your views here.



def check(request):
    return HttpResponse("from event")

def home(request):
    events = Event.objects.select_related("category")
    today = date.today()
    up_events = events.filter(date__gte=today)
    context = {
        "up_events": up_events,
    }
    return render(request,"home.html",context)


def dashboard(request):
    
    type = request.GET.get('type','all')
    search = request.GET.get('q', '')
    print(type)
    
    
    events = Event.objects.select_related("category")
    today = date.today()

    up_events = events.filter(date__gte=today)
    past_events = events.filter(date__lt=today)
    
    base_query = Event.objects.select_related("category")
    
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







def update_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == "POST":
        form = EventModelForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect("dashboard")
    else:
        form = EventModelForm(instance=event)

    context = {
        "form": form,
    }
    
    return render(request, "user-input/event-form.html", context)



def delete_event(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request,"Event Deleted succesfully!")
        return redirect("dashboard")
    
    else:
        messages.error(request,"something went wrong!")
        return redirect("dashboard")
            
    