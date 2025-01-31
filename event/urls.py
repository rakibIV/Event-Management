from django.urls import path
from event.views import check,dashboard,book_now,navbar

urlpatterns = [
    path("check/",check),
    path("dashboard/",dashboard,name="dashboard"),
    path("book_now/",book_now, name="book_now"),
    path("navbar/",navbar),
]