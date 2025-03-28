from django.urls import path
from core.views import no_permission, redirect_to_dashboard,dummy_page,home

urlpatterns = [
    path("no-permission/",no_permission,name="no-permission"),
    path("redirect-dashboard/",redirect_to_dashboard,name="redirect-dashboard"),
    path("dummy/",dummy_page,name="dummy"),
    path('',home,name='home')
]
