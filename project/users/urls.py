from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .views import SignUpView, UserProfileView
from .forms import CustomPasswordChangeForm

app_name = "users"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/<slug:username>", UserProfileView.as_view(), name="profile"),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            template_name="users/password_change.html",
            form_class=CustomPasswordChangeForm,
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password_change_done",
    ),
]
