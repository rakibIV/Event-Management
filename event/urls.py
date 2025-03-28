from django.urls import path
from event.views import check,book_now,create_event,add_category,category_page,update_event,delete_event,dashboard,rsvp_now, update_category,delete_category,event_details

urlpatterns = [
    path("check/",check),

    path("dashboard/",dashboard,name="dashboard"),
    path("book_now/",book_now, name="book_now"),
    path("create_event/",create_event,name="create_event"),
    path("event-details/<int:id>/",event_details,name="event-details"),
    path("add_category/",add_category,name="add_category"),
    path("update_category/<int:id>/",update_category,name="update_category"),
    path("delete_category/<int:id>/",delete_category,name="delete_category"),
    path("update_event/<int:id>/",update_event,name="update_event"),
    path("delete_event/<int:id>/",delete_event,name="delete_event"),
    path("rsvp-now/<int:event_id>/",rsvp_now,name="rsvp-now"),
    path("category-page/",category_page,name="category-page"),
]