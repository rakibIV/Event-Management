from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import Group, Permission
from users.forms import CustomRegistrationForm, AssignRoleForm, PassChangeForm, PassResetForm, PassResetConfirmForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from event.models import Event,Category
from django.db.models import Count
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User = get_user_model()
from users.forms import UserProfileForm
from users.models import CustomUser


# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_user(user):
    return user.groups.filter(name='User').exists()



def sign_up(request):
    form = CustomRegistrationForm()
        
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request,"A confirmation mail sent. Please check your email")
            return redirect('sign-in')
        else:
            print("Form is not valid")
    context = {
        "form":form
    }
    return render(request,'Registration/register.html',context)


class SignUpView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'Registration/register.html'
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        user = form.save(commit=False)  
        if form.cleaned_data['password1'] != form.cleaned_data['confirm_password']:
            return self.form_invalid(form)
        user.set_password(form.cleaned_data['password1'])  
        user.save()
        messages.success(self.request, "A confirmation email has been sent. Please check your email.")
        return super().form_valid(form)
    

class CustomLoginView(LoginView):
    template_name = 'Registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def post(self, request, *args, **kwargs):
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
           
            login(request, user)
            return redirect(self.get_success_url())

        else:
            messages.error(request, "Username or password is incorrect.")
            return render(request, self.template_name)
        
    def get_success_url(self):
        return self.request.GET.get('next') or self.success_url

        


    
class LogoutView(LogoutView,LoginRequiredMixin):
    login_url = 'sign-in'
    
def activate_user(request,user_id,token):
    user = User.objects.get(id=user_id)
    try :
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request,"Your account is activated. Please login")
            return redirect('sign-in')
        else :
            messages.error(request,"Invalid token")
            return redirect('sign-in')
    except Exception as e:
        messages.error(request,"Invalid token")
        return redirect('sign-in')
    
    
    
@login_required(login_url='sign-in')
@user_passes_test(is_user,login_url='no-permission')
def user_dashboard(request):
    today = date.today()
    base_query = request.user.events.all()
    events = base_query
    past_events = base_query.filter(date__lt=today)
    upcoming_events = base_query.filter(date__gt=today)
    context ={
        "past_events":past_events,
        "events":events,
        "upcoming_events":upcoming_events
        }
    return render(request,'user_dashboard.html',context)


@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    events = Event.objects.select_related('category').prefetch_related('participants')
    upcoming_events = events.filter(date__gt=date.today())
    categories = Category.objects.annotate(
        event_count=Count('events', distinct=True)
    )
    users = User.objects.prefetch_related('groups')
    participants = User.objects.filter(events__isnull=False).annotate(
        event_count=Count('events', distinct=True)
    ).distinct()
    groups = Group.objects.prefetch_related('permissions')
    context = {
        "events":events,
        "upcoming_events":upcoming_events,
        "categories":categories,
        "users":users,
        "participants":participants,
        "groups":groups
    }
    return render(request,'admin_dashboard.html',context)

@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    user = User.objects.get(id=user_id)
    groups = Group.objects.all()
    if request.method=="POST":
        group_id = request.POST.get('group')
        group = Group.objects.get(id=group_id)
        user.groups.clear()
        user.groups.add(group)
        return redirect('admin-dashboard')
    
    context = {
        "groups":groups,
        "user":user
    }
    
    return render(request,'assign_role.html',context)


@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def edit_group(request,group_id):
    group = Group.objects.get(id=group_id)
    all_permissions = Permission.objects.all()
    current_permissions = group.permissions.all()
    if request.method == "POST":
        selected_permissions = request.POST.getlist('permissions')
        group.permissions.clear()
        for perm_id in selected_permissions:
            permission = Permission.objects.get(id=perm_id)
            group.permissions.add(permission)
        group_name = request.POST.get('group_name')
        if group_name and group_name != group.name:
            group.name = group_name
            group.save()
        return redirect('admin-dashboard')
        
    context = {
        'group': group,
        'all_permissions': all_permissions,
        'current_permissions': current_permissions
    }
    
    return render(request, 'edit_group.html', context)
    
    
    
    
@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    all_permissions = Permission.objects.all()
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        selected_permissions = request.POST.getlist('permissions')
        
        
        if Group.objects.filter(name=group_name).exists():
            messages.error(request, "A group with this name already exists")
            return render(request, 'create_group.html', {
                'permissions': all_permissions
            })
        
        
        new_group = Group.objects.create(name=group_name)
        
        for perm_id in selected_permissions:
            permission = Permission.objects.get(id=perm_id)
            new_group.permissions.add(permission)
        
        return redirect('admin-dashboard') 
        
        
    
    return render(request, 'create_group.html', {
        'permissions': all_permissions,
    })
    

@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def delete_group(request,id):
    if request.method=="POST":
        group = Group.objects.get(id=id)
        group.delete()
        return redirect("redirect-dashboard")
    

@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def delete_participants(request,id):
    if request.method == "POST":
        user = User.objects.get(id=id)
        user.events.clear()
        return redirect("redirect-dashboard")
    
    


class UserProfileView(LoginRequiredMixin, UpdateView):
    """User profile view"""
    login_url = 'sign-in'
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'account/user_profile.html'
    success_url = reverse_lazy('user-profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
    
    
    
class CustomPasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    template_name = 'account/password_change.html'
    form_class = PassChangeForm
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/reset_password.html'
    form_class = PassResetForm
    success_url = reverse_lazy('user-profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context    
    
    def form_valid(self, form):
        messages.success(self.request, "Password reset email sent. Please check your email.")
        return super().form_valid(form)
    
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/reset_confirm.html'
    form_class = PassResetConfirmForm
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        messages.success(self.request, "Password reset Successfully!")
        return super().form_valid(form)
    