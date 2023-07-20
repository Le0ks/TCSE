from django.contrib import auth, messages
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import SignUpForm
from .models import Profile


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = SignUpForm

    def get_success_url(self):
        return reverse("homepage:home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        profile = Profile(user=user)
        profile.save()
        auth.login(self.request, user)
        messages.success(self.request, "Спасибо за регистрацию!")
        return super().form_valid(form)


class UserProfileView(TemplateView):
    template_name = "users/profile.html"
