import django.conf
import django.contrib
import django.contrib.auth
import django.contrib.auth.mixins
import django.contrib.auth.tokens
import django.contrib.auth.views
import django.contrib.messages
import django.contrib.sites.shortcuts
import django.db.models
import django.http
import django.shortcuts
import django.urls
import django.utils.encoding
import django.utils.http
import django.views
import django.views.generic
import django.views.generic.edit
import users.backends
import users.forms
import users.mixins
import users.models
import users.tasks
import users.tokens


class SignupView(django.views.generic.edit.FormView):
    """регистрация пользователя"""

    form_class = users.forms.SignUpForm
    template_name = "users/signup.html"

    def get_success_url(self) -> str:
        """получаем адрес для редиректа в случае валидной формы"""
        return django.urls.reverse(
            "homepage:home",
        )

    def form_valid(
        self, form: users.forms.SignUpForm
    ) -> django.http.HttpResponsePermanentRedirect:
        """
        при валидной форме создается новый пользователь
        и активируется(сразу или письмо для активации приходит на почту)
        """
        user = form.save(commit=False)
        user.is_active = django.conf.settings.USER_IS_ACTIVE
        user.save()
        profile = users.models.Profile(user=user)
        profile.save()
        if not django.conf.settings.USER_IS_ACTIVE:
            token_generator = (
                django.contrib.auth.tokens.default_token_generator
            )
            users.tasks.send_email_with_token(
                user_id=user.pk,
                template_name="users/emails/activate_user.html",
                subject="Активация аккаунта",
                where_to="users:activate_user",
                protocol="https" if self.request.is_secure() else "http",
                domain=django.contrib.sites.shortcuts.get_current_site(
                    self.request
                ).domain,
                token=token_generator.make_token(user),
            )
            django.contrib.messages.success(
                self.request,
                f"На вашу почту {user.email} было "
                "отправлено письмо с активацией",
            )
        else:
            django.contrib.messages.success(
                self.request, "Спасибо за регистрацию!"
            )
            django.contrib.auth.login(
                self.request, user, backend="users.backends.EmailBackend"
            )
        return super().form_valid(form)


class ActivateUserView(django.views.generic.View):
    """Активирует аккаунт пользователя"""

    def get(
        self, request: django.http.HttpRequest, uidb64: str, token: str
    ) -> django.http.HttpResponse:
        """
        активация аккаунта пользователя
        если токен валидный
        """
        try:
            user = users.models.User.objects.get(
                pk=django.utils.encoding.force_str(
                    django.utils.http.urlsafe_base64_decode(uidb64)
                )
            )
        except Exception:
            user = None
        if (
            user
            and django.contrib.auth.tokens.default_token_generator.check_token(
                user, token
            )
        ):
            user.is_active = True
            user.save()
            django.contrib.auth.login(
                request, user, backend="users.backends.EmailBackend"
            )
            django.contrib.messages.success(
                request, "Спасибо за активацию аккаунта"
            )
        else:
            django.contrib.messages.error(request, "Ссылка активации неверна.")
        return django.shortcuts.redirect("homepage:home")


class ResetLoginAttemptsView(django.views.generic.View):
    def get(
        self, request: django.http.HttpRequest, uidb64: str, token: str
    ) -> django.http.HttpResponsePermanentRedirect:
        """реактивация аккаунта после превышения попыток входа"""
        try:
            user = users.models.User.objects.get(
                pk=django.utils.encoding.force_str(
                    django.utils.http.urlsafe_base64_decode(uidb64)
                )
            )
        except Exception:
            user = None
        if user and users.tokens.token_7_days.check_token(user, token):
            user.is_active = True
            django.contrib.messages.success(
                request,
                "Спасибо за активацию аккаунта," "теперь вы можете войти",
            )
            user.login_attempts = django.conf.settings.LOGIN_ATTEMPTS - 1
            user.save()
        else:
            django.contrib.messages.error(request, "Ссылка активации неверна.")
        return django.shortcuts.redirect("homepage:home")


class UserProfileView(django.views.generic.DetailView):
    context_object_name = "user"
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        return users.models.User.objects.get_only_useful_detail_fields().get(
            username=self.kwargs["username"]
        )


class UserProfileChangeView(
    users.mixins.UsernameMixinView,
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    template_name = "users/change.html"

    def get(
        self, request: django.http.HttpRequest, username: str
    ) -> django.http.HttpResponse:
        if request.user.username == username:
            user_form = users.forms.CustomUserChangeForm(instance=request.user)
            profile_form = users.forms.ProfileChangeForm(
                instance=request.user.profile
            )
            context = {
                "forms": [user_form, profile_form],
            }
            return django.shortcuts.render(
                request, self.template_name, context=context
            )
        raise django.http.Http404()

    def post(
        self, request: django.http.HttpRequest, username: str
    ) -> django.http.HttpResponsePermanentRedirect:
        if request.user.username == username:
            user_form = users.forms.CustomUserChangeForm(
                request.POST, instance=request.user
            )
            profile_form = users.forms.ProfileChangeForm(
                request.POST, request.FILES, instance=request.user.profile
            )
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                django.contrib.messages.success(
                    request, "Профиль успешно изменен!"
                )
                return django.shortcuts.redirect("users:profile", username)
            else:
                return django.shortcuts.render(
                    request,
                    self.template_name,
                    {"forms": [user_form, profile_form]},
                )
        raise django.http.Http404()
