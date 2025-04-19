from django.shortcuts import render,redirect
from django.http import HttpResponse
from event.forms import EventModelForm,CategoryModelForm
from django.contrib import messages
from event.models import Event, Category
from datetime import date
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test
from users.views import is_admin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


def is_manager(user):
    return user.groups.filter(name="Organizer").exists()

def is_manager_or_admin(user):
    flag = is_manager(user) or is_admin(user)
    print("flag:",flag)
    return is_manager(user) or is_admin(user)




def check(request):
    return HttpResponse("from event")

@login_required(login_url='sign-in')
@user_passes_test(is_manager_or_admin,login_url='no-permission')
def dashboard(request):
    
    type = request.GET.get('type','all')
    search = request.GET.get('q', '')
    print("printing from event.....")
    
    
    events = Event.objects.select_related('category').prefetch_related('participants')
    participants = User.objects.filter(events__isnull=False).distinct()
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
        "partcipants":participants
    }
    
    return render(request,"dashboard.html",context)
    




class CreateEventView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'user-input/event-form.html'
    login_url = 'sign-in'
    success_url = reverse_lazy('redirect-dashboard')
    
    def test_func(self):
        return is_manager_or_admin(self.request.user)
    def handle_no_permission(self):
        return redirect('no-permission')




class UpdateEventView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = 'user-input/event-form.html'
    login_url = 'sign-in'
    success_url = reverse_lazy('redirect-dashboard')
    pk_url_kwarg = 'id'
    def test_func(self):
        return is_manager_or_admin(self.request.user)
    def handle_no_permission(self):
        return redirect('no-permission')



@login_required(login_url='sign-in')
@user_passes_test(is_manager_or_admin,login_url='no-permission')
def delete_event(request,id):
    if request.method == 'POST':
        print("inside delete event.......")
        event = Event.objects.get(id=id)
        event.delete()
        
        # messages.success(request,"Event Deleted succesfully!")
        return redirect("redirect-dashboard")
    
    else:
        # messages.error(request,"something went wrong!")
        return redirect("redirect-dashboard")
    
    
class DeleteEventView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Event
    success_url = reverse_lazy('redirect-dashboard')
    login_url = 'sign-in'
    pk_url_kwarg = 'id'
    
    def test_func(self):
        return is_manager_or_admin(self.request.user)
    def handle_no_permission(self):
        return redirect('no-permission')




@login_required(login_url='sign-in')
@user_passes_test(is_manager_or_admin,login_url='no-permission')
def add_category(request):
    form = CategoryModelForm()
    if request.method == "POST":
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request,"Category added successfully!")
            return redirect("add_category")
        
    context = {
        "form" : form,
    }
    
    return render(request,"user-input/category-form.html",context)


@login_required(login_url='sign-in')
@user_passes_test(is_manager_or_admin,login_url='no-permission')
def update_category(request,id):
    category = Category.objects.get(id=id)
    form = CategoryModelForm(instance=category)
    if request.method == "POST":
        form = CategoryModelForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            # messages.success(request,"Category added successfully!")
            return redirect("add_category")
        
    context = {
        "form" : form,
    }
    
    return render(request,"user-input/category-form.html",context)








@login_required(login_url='sign-in')
@user_passes_test(is_manager_or_admin,login_url='no-permission')
def delete_category(request,id):
    if request.method == 'POST':
        print("inside delete event.......")
        category = Category.objects.get(id=id)
        category.delete()
        # messages.success(request,"Category Deleted succesfully!")
        return redirect("redirect-dashboard")
    
    else:
        # messages.error(request,"something went wrong!")
        print("Something went wrong in deleting category")
        return redirect("redirect-dashboard")





    
@login_required(login_url='sign-in')
def rsvp_now(request,event_id):
    event = Event.objects.get(id=event_id)
    if request.method=="POST":
        if request.user in event.participants.all():
            print("rsvp removing.....")
            event.participants.remove(request.user)
        else:
            print("rsvp adding.....")
            event.participants.add(request.user)
            return redirect("home")
    return redirect("home")



def event_details(request,id):
    event = Event.objects.get(id=id)
    return render(request,'event_details.html',{"event":event})

@login_required(login_url='sign-in')
@user_passes_test(is_manager_or_admin,login_url='no-permission')
def category_page(request):
    categories = Category.objects.prefetch_related("events").all()
    return render(request,"delete_category.html",{"categories":categories})
            
            
            

    