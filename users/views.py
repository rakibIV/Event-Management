from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from users.forms import CustomRegistrationForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator


# Create your views here.


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
        
    return render(request,'registration/login.html', {})



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