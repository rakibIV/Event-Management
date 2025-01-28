from django.urls import path
from event.views import check,dashboard

urlpatterns = [
    path("check/",check),
    path("dashboard/",dashboard)
]