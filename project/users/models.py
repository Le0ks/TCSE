import transliterate
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from users.managers import UserManager


def generate_image_path(obj: models.Model, filename: str) -> str:
    filename = transliterate.translit(filename, "ru", reversed=True)
    return f"users/{obj.user.pk}/{filename}"


class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField(
        verbose_name="почта",
        help_text="Электронная почта пользователя",
        blank=True,
        max_length=100,
        unique=True,
    )
    login_attempts = models.IntegerField(
        default=0,
        verbose_name="неудачные попытки",
        help_text="Количество неудачных попыток входа в аккаунт",
    )

    class Meta(AbstractUser.Meta):
        db_table = "auth_user"
        swappable = "AUTH_USER_MODEL"

    def get_absolute_url(self) -> str:
        return reverse_lazy("users:profile", kwargs={"pk": self.pk})


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        verbose_name="профиль",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        blank=True,
        verbose_name="аватарка",
        help_text="Аватарка пользователя",
        upload_to=generate_image_path,
        null=True,
    )

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return self.user.username
