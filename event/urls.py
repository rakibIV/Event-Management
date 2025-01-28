from django.urls import path
from event.views import check

urlpatterns = [
    path("check/",check)
]