from django.urls import path
from event.views import check,home,book_now,navbar,create_event,add_category,update_event,delete_event,dashboard

urlpatterns = [
    path("check/",check),
    path("home/",home,name="home"),
    path("dashboard/",dashboard,name="dashboard"),
    path("book_now/",book_now, name="book_now"),
    path("navbar/",navbar),
    path("create_event/",create_event,name="create_event"),
    path("add_category/",add_category,name="add_category"),
    path("update_event/<int:id>/",update_event,name="update_event"),
    path("delete_event/<int:id>/",delete_event,name="delete_event"),
]