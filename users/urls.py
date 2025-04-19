from django.urls import path
from users.views import UserProfileView, SignUpView,CustomLoginView,LogoutView,activate_user,user_profile,user_dashboard,admin_dashboard,assign_role,delete_group,edit_group, create_group,delete_participants
urlpatterns = [
    path("sign-up/",SignUpView.as_view(),name="sign-up"),
    path("sign-in/",CustomLoginView.as_view(),name="sign-in"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("activate/<int:user_id>/<str:token>",activate_user),
    path("user-dashboard/",user_dashboard,name="user-dashboard"),
    path("admin-dashboard/",admin_dashboard,name="admin-dashboard"),
    path("assign-role/<int:user_id>/",assign_role,name="assign-role"),
    path("update-group/<int:group_id>/",edit_group,name="update-group"),
    path("create-group/",create_group,name="create-group"),
    path("delete-group/<int:id>/",delete_group,name="delete-group"),
    path("delete-participants/<int:id>/",delete_participants,name="delete-participants"),
    path("user-profile/",UserProfileView.as_view(),name="user-profile"),
]
