import django.contrib.auth.views
from django.urls import path, reverse_lazy
import users.forms
import users.views


app_name = "users"

urlpatterns = [
    path(
        "login/",
        django.contrib.auth.views.LoginView.as_view(
            template_name="users/login.html",
            form_class=users.forms.CustomAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(
            template_name="users/login.html"
        ),
        name="logout",
    ),
    path(
        "signup/", users.views.SignupView.as_view(), name="signup"
    ),
    path(
        "user/<slug:username>",
        users.views.UserProfileView.as_view(),
        name="profile",
    ),
    path(
        "user/<slug:username>/password_change/",
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            form_class=users.forms.CustomPasswordChangeForm,
            success_url=reverse_lazy("users:profile")
        ),
        name="password_change",
    ),
    path(
        "user/<slug:username>/password_reset/",
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            form_class=users.forms.CustomPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "user/<slug:username>/password_reset/done/",
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "user/<slug:username>/reset/<uidb64>/<token>/",
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            form_class=users.forms.CustomSetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "user/<slug:username>/reset/done/",
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "activate/<uidb64>/<token>/",
        users.views.ActivateUserView.as_view(),
        name="activate_user",
    ),
    path(
        "user/<slug:username>/change/",
        users.views.UserProfileChangeView.as_view(),
        name="profile_change",
    ),
    path(
        "reset_login_attempts/<uidb64>/<token>/",
        users.views.ResetLoginAttemptsView.as_view(),
        name="reset_login_attempts",
    ),
]
