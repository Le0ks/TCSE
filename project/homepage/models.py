from django.db import models
import transliterate


def generate_image_path(obj, filename):
    filename = transliterate.translit(filename, "ru", reversed=True)
    return f"news/{filename}"


class New(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="новость",
        help_text="Введите название новости"
    )
    text = models.TextField(
        verbose_name="текст новости",
        help_text="Введите текст новости"
    )
    image = models.ImageField(
        verbose_name="фото",
        blank=True,
        null=True,
        upload_to=generate_image_path
    )
    time = models.DateTimeField(
        verbose_name="время публикации",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "новости"
