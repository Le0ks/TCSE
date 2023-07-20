from django.db import models
from users.models import User


class Feedback(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "получено"
        PROCESSING = "processing", "в обработке"
        ANSWERED = "answered", "ответ дан"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(
        "текст обратной связи",
        help_text="Что вы хотите сообщить нам",
    )
    created_on = models.DateTimeField("дата создания", auto_now_add=True)
    status = models.CharField(
        "статус обработки",
        help_text="Какой статус сейчас имеет отзыв",
        max_length=16,
        choices=Status.choices,
        default=Status.RECEIVED,
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратная связь"
