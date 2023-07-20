from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="почта",
        help_text="Электронная почта пользователя",
        blank=True,
        max_length=100,
        unique=True,
    )

    class Meta(AbstractUser.Meta):
        db_table = "auth_user"
        swappable = "AUTH_USER_MODEL"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        verbose_name="профиль",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return self.user.username
