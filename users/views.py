from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User, Group, Permission
from users.forms import CustomRegistrationForm, AssignRoleForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from event.models import Event,Category
from django.db.models import Count
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models


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
# 

def sign_in(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print("doc:",username,password)
        
        user = authenticate(request,username=username,password=password)
        print("user:",user)
        
        if user:
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request,"Username or password is incorrect")
        
    return render(request,'Registration/login.html', {})


@login_required(login_url='sign-in')
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    
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
    