from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user,user_dashboard,admin_dashboard,assign_role,delete_group,edit_group, create_group,delete_participants
urlpatterns = [
    path("sign-up/",sign_up,name="sign-up"),
    path("sign-in/",sign_in,name="sign-in"),
    path("logout/",sign_out,name="logout"),
    path("activate/<int:user_id>/<str:token>",activate_user),
    path("user-dashboard/",user_dashboard,name="user-dashboard"),
    path("admin-dashboard/",admin_dashboard,name="admin-dashboard"),
    path("assign-role/<int:user_id>/",assign_role,name="assign-role"),
    path("update-group/<int:group_id>/",edit_group,name="update-group"),
    path("create-group/",create_group,name="create-group"),
    path("delete-group/<int:id>/",delete_group,name="delete-group"),
    path("delete-participants/<int:id>/",delete_participants,name="delete-participants"),
]
