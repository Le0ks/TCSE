import string
from django.db import models
from django.shortcuts import reverse
from django.utils.crypto import get_random_string
from users.models import User


def event_directiry_path(instance, filename):
    return f"events/{instance.event.slug}/event/{filename}"


def task_directiry_path(instance, filename):
    return f"events/{instance.task.event.slug}/tasks/{filename}"


def answer_directiry_path(instance, filename):
    return f"events/{instance.answer.task.event.slug}/answers/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="категория")
    description = models.TextField(verbose_name="описание")
    is_published = models.BooleanField(
        verbose_name="опубликован", default=False
    )
    slug = models.SlugField(verbose_name="url", unique=True, null=True)
    image = models.ImageField(
        verbose_name="фото", null=True, blank=True, upload_to="categories"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Event(models.Model):
    class AnswerRule(models.IntegerChoices):
        MOMENT_ANSWER = 0, "Моментальный вывод правильных ответов"
        SECRET_ANSWER = 1, "Секретные правильные ответы"
        AFTER_ANSWER = (
            2,
            "Вывод правильных ответов после прохождения мероприятия",
        )

    class TimeType(models.IntegerChoices):
        ETERNAL = 0, "Мероприятия без ограничений по времени"
        ETERNAL_DURATION = (
            1,
            "Мероприятия только с ограничением по времени его прохождения",
        )
        START_FINISH = 2, "Мероприятия с началом и концом"
        START_FINISH_DURATION = (
            3,
            "Мероприятия с началом и концом и с "
            "ограничением по времени его прохождения",
        )

    name = models.CharField(
        max_length=150,
        verbose_name="название мероприятия",
    )
    slug = models.SlugField(verbose_name="слаг", unique=True, null=True)
    description = models.TextField(
        verbose_name="описание мероприятия",
    )
    is_published = models.BooleanField(
        default=False, verbose_name="опубликовано"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="автор",
        related_name="event_author",
        help_text="Организатор мероприятия",
        null=True,
    )
    start_time = models.DateTimeField(
        verbose_name="время начала мероприятия", null=True, blank=True
    )
    finish_time = models.DateTimeField(
        verbose_name="время конца мероприятия", null=True, blank=True
    )
    category = models.ForeignKey(
        Category, verbose_name="категория", on_delete=models.CASCADE
    )
    is_private = models.BooleanField(
        verbose_name="закрытое мероприятие",
        default=False,
    )
    is_ended = models.BooleanField(
        verbose_name="подведены ли итоги", default=False
    )
    answer_rule = models.IntegerField(
        verbose_name="виды мероприятий в зависимости"
        " от типа вывода правильного ответа",
        choices=AnswerRule.choices,
        default=0,
    )
    type_by_time = models.IntegerField(
        verbose_name="выбор типа времени мероприятия",
        choices=TimeType.choices,
        default=0,
    )
    duration = models.PositiveIntegerField(
        help_text="Укажите продолжительность мероприятия в минутах",
        null=True,
        blank=True,
        verbose_name="продолжительность",
    )
    image = models.ImageField(
        "изображение", upload_to=event_directiry_path, default=None
    )
    secret_key = models.CharField(
        default=get_random_string(
            20, string.ascii_letters + string.digits + string.punctuation
        ),
        unique=True,
        max_length=30,
    )

    def get_absolute_url(self):
        return reverse(
            "events:event_detail",
            kwargs={
                "category_name": self.category.slug,
                "event_name": self.slug,
            },
        )

    def get_result_url(self):
        return reverse(
            "events:event_result",
            kwargs={
                "category_name": self.category.slug,
                "event_name": self.slug,
            },
        )

    def get_rating_url(self):
        return reverse(
            "events:event_rating",
            kwargs={
                "category_name": self.category.slug,
                "event_name": self.slug,
            },
        )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "мероприятие"
        verbose_name_plural = "мероприятия"
        ordering = ("category",)


class EventImageBaseModel(models.Model):
    image = models.ImageField(
        "изображение", upload_to=event_directiry_path, default=None
    )

    class Meta:
        abstract = True


class EventMainImage(EventImageBaseModel):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="main_image",
    )

    def __str__(self):
        return self.event.name

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class EventGallery(EventImageBaseModel):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="gallery"
    )

    class Meta:
        verbose_name = "фотогалерея"
        verbose_name_plural = "фотогалереи"


class EventResults(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="пользователь",
        help_text="Пользователь, участвовавший в мероприятии",
        on_delete=models.CASCADE,
    )
    event = models.ForeignKey(
        Event,
        verbose_name="мероприятие",
        help_text="мероприятие, к которому относится результат",
        on_delete=models.CASCADE,
    )
    number_of_points = models.PositiveIntegerField(
        verbose_name="количество набранных баллов", default=0
    )
    is_ended = models.BooleanField(
        default=False,
        help_text="Завершено ли мероприятие?",
        verbose_name="завершено",
    )
    is_correct_secret_key = models.BooleanField(default=False)

    class Meta:
        verbose_name = "результат"
        verbose_name_plural = "результаты"


class Task(models.Model):
    class TaskType(models.IntegerChoices):
        TEST_TASK = 0, "тестовое задание"
        CONTROL_TASK = 1, "письменное задание"
        FILE_TASK = 2, "файловое задание"

    text = models.TextField(verbose_name="текст задания")
    comment = models.TextField(verbose_name="комментарий к заданию")
    event = models.ForeignKey(
        Event,
        verbose_name="мероприятие",
        related_name="event_task",
        on_delete=models.CASCADE,
    )
    number_of_points = models.PositiveIntegerField(
        verbose_name="количество баллов", default=1
    )
    task_type = models.IntegerField(
        verbose_name="тип задания", choices=TaskType.choices, default=0
    )
    image = models.ImageField(
        "изображение", upload_to=task_directiry_path, default=None
    )

    class Meta:
        verbose_name = "задание"
        verbose_name_plural = "задания"

    def __str__(self):
        return self.text


class Tag(models.Model):
    name = models.CharField(
        verbose_name="имя тега", max_length=150, help_text="Введите имя тега"
    )
    is_published = models.BooleanField(
        verbose_name="опубликован",
        default=False,
        help_text="Опубликован тег или нет",
    )
    task = models.ForeignKey(
        Task,
        related_name="task_tags",
        verbose_name="тэги задания",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"


class Answer(models.Model):
    text = models.CharField(verbose_name="ответ", max_length=150)
    is_correct = models.BooleanField(
        verbose_name="правильный ли ответ", default=False
    )
    comment = models.TextField(
        verbose_name="комментарий к ответу ", null=True, blank=True
    )
    task = models.ForeignKey(
        Task,
        verbose_name="задание",
        on_delete=models.CASCADE,
        related_name="answers",
    )
    image = models.ImageField(
        "изображение", upload_to=answer_directiry_path, default=None
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"


class UserAnswer(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        related_name="user_answers",
        help_text="пользователь, который дал ответ",
        null=True,
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(verbose_name="правильность ответа")

    def __str__(self):
        return self.answer.text

    class Meta:
        verbose_name = "ответ пользователя"
        verbose_name = "ответы пользователя"


class Post(models.Model):
    event = models.ForeignKey(
        Event, verbose_name="пост", on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name="текст поста")
    # image = models.ImageField(verbose_name="фотографии")
    is_published = models.BooleanField(verbose_name="опубликовано")


class Comment(models.Model):
    post = models.ForeignKey(
        Post, verbose_name="комментарии", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        related_name="user_commentor",
        help_text="пользователь, который оставил комментарий",
    )
    text = models.TextField(verbose_name="текст комментария")
