from django.db import models
from users.models import User
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="категория")
    description = models.TextField(verbose_name="описание")
    is_published = models.BooleanField(verbose_name="опубликован", default=False)
    slug = models.SlugField(verbose_name="url", unique=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Event(models.Model):
    class AnswerRule(models.IntegerChoices):
        MOMENT_ANSWER = 0, "Моментальный вывод правильных ответов"
        SECRET_ANSWER = 1, "Секретные правильные ответы"
        AFTER_ANSWER = 2, "Вывод правильных ответов после прохождения мероприятия"

    class TimeType(models.IntegerChoices):
        ETERNAL = 0, "Мероприятия без ограничений по времени"
        ETERNAL_DURATION = (
            1,
            "Мероприятия только с ограничением по времени его прохождения",
        )
        START_FINISH = 2, "Мероприятия с началом и концом"
        START_FINISH_DURATION = (
            3,
            "Мероприятия с началом и концом и с ограничением по времени его прохождения",
        )

    name = models.CharField(
        max_length=150,
        verbose_name="название мероприятия",
    )
    slug = models.SlugField(verbose_name="слаг", unique=True, null=True)
    description = models.TextField(
        verbose_name="описание мероприятия",
    )
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")
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
    is_ended = models.BooleanField(verbose_name="подведены ли итоги", default=False)
    answer_rule = models.IntegerField(
        verbose_name="виды мероприятий в зависимости от типа вывода правильного ответа",
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
    solved = models.PositiveIntegerField(
        verbose_name="задачи", help_text="Верно решенные задачи", default=0
    )
    is_ended = models.BooleanField(
        default=False, help_text="Завершено ли мероприятие?", verbose_name="завершено"
    )

    class Meta:
        verbose_name = "результат"
        verbose_name_plural = "результаты"


class Task(models.Model):
    text = models.TextField(verbose_name="текст задания")
    event = models.ForeignKey(
        Event,
        verbose_name="мероприятие",
        related_name="event_task",
        on_delete=models.CASCADE,
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
        verbose_name="опубликован", default=False, help_text="Опубликован тег или нет"
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
    is_correct = models.BooleanField(verbose_name="правильный ли ответ", default=False)
    comment = models.TextField(
        verbose_name="комментарий к ответу", null=True, blank=True
    )
    task = models.ForeignKey(
        Task, verbose_name="задание", on_delete=models.CASCADE, related_name="answers"
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
    event = models.ForeignKey(Event, verbose_name="пост", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="текст поста")
    # image = models.ImageField(verbose_name="фотографии")
    is_published = models.BooleanField(verbose_name="опубликовано")


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name="комментарии", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        related_name="user_commentor",
        help_text="пользователь, который оставил комментарий",
    )
    text = models.TextField(verbose_name="текст комментария")
