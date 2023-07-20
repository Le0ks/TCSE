from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)

from .models import User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "password1", "password2")
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["username"].help_text = "Введите ваш username"
        "Только буквы, цифры и символы @/./+/-/_."

        self.fields["email"].label = "Почта"
        self.fields["email"].help_text = "Введите адрес электронной почты"

        self.fields["password1"].label = "Пароль"
        self.fields["password1"].help_text = "Придумайте пароль"

        self.fields["password2"].label = "Пароль ещё раз"
        self.fields["password2"].help_text = "Подтвердите пароль"


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Имя пользователя"
        self.fields["username"].help_text = "Введите имя польвователя"

        self.fields["password"].label = "Пароль"
        self.fields["password"].help_text = "Введите пароль"


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "Старый пароль"
        self.fields["old_password"].help_text = "Введите старый пароль"

        self.fields["new_password1"].label = "Новый пароль"
        self.fields["new_password1"].help_text = "Придумайте пароль"

        self.fields["new_password2"].label = "Пароль еще раз"
        self.fields["new_password2"].help_text = "Подтвердите пароль"
