from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("Hello World!")


def check(request):
    return HttpResponse("from event")

def dashboard(request):
    return render(request,"dashboard.html")
