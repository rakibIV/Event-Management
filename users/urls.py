from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeDoneView
from users.views import UserProfileView, SignUpView,CustomLoginView,LogoutView,CustomPasswordChangeView,CustomPasswordResetView,CustomPasswordResetConfirmView,activate_user,user_dashboard,admin_dashboard,assign_role,delete_group,edit_group, create_group,delete_participants
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
    path("password_change/",CustomPasswordChangeView.as_view(),name="password-change"),
    path("password_change_done/",PasswordChangeDoneView.as_view(template_name = 'account/password_change_done.html'),name="password_change_done"),
    path("password_reset/",CustomPasswordResetView.as_view(),name="password-reset"),
    path("password_reset/confirm/<uidb64>/<token>/",CustomPasswordResetConfirmView.as_view(), name= "password_reset_confirm"),
]
