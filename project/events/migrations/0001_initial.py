# Generated by Django 4.2 on 2023-12-18 19:22

from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'text',
                    models.CharField(max_length=150, verbose_name='ответ'),
                ),
                (
                    'is_correct',
                    models.BooleanField(
                        default=False, verbose_name='правильный ли ответ'
                    ),
                ),
                (
                    'comment',
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name='комментарий к ответу ',
                    ),
                ),
            ],
            options={
                'verbose_name': 'ответ',
                'verbose_name_plural': 'ответы',
            },
        ),
        migrations.CreateModel(
            name='AnswerImage',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        default=None,
                        upload_to=events.models.answer_directiry_path,
                        verbose_name='изображение',
                    ),
                ),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=150, verbose_name='категория'),
                ),
                ('description', models.TextField(verbose_name='описание')),
                (
                    'is_published',
                    models.BooleanField(
                        default=False, verbose_name='опубликован'
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        null=True, unique=True, verbose_name='url'
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to='categories',
                        verbose_name='фото',
                    ),
                ),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='текст комментария')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=150, verbose_name='название мероприятия'
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        null=True, unique=True, verbose_name='слаг'
                    ),
                ),
                (
                    'description',
                    models.TextField(verbose_name='описание мероприятия'),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=False, verbose_name='опубликовано'
                    ),
                ),
                (
                    'start_time',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name='время начала мероприятия',
                    ),
                ),
                (
                    'finish_time',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name='время конца мероприятия',
                    ),
                ),
                (
                    'is_private',
                    models.BooleanField(
                        default=False, verbose_name='закрытое мероприятие'
                    ),
                ),
                (
                    'is_ended',
                    models.BooleanField(
                        default=False, verbose_name='подведены ли итоги'
                    ),
                ),
                (
                    'answer_rule',
                    models.IntegerField(
                        choices=[
                            (0, 'Моментальный вывод правильных ответов'),
                            (1, 'Секретные правильные ответы'),
                            (
                                2,
                                'Вывод правильных ответов после прохождения мероприятия',
                            ),
                        ],
                        default=0,
                        verbose_name='виды мероприятий в зависимости от типа вывода правильного ответа',
                    ),
                ),
                (
                    'type_by_time',
                    models.IntegerField(
                        choices=[
                            (0, 'Мероприятия без ограничений по времени'),
                            (
                                1,
                                'Мероприятия только с ограничением по времени его прохождения',
                            ),
                            (2, 'Мероприятия с началом и концом'),
                            (
                                3,
                                'Мероприятия с началом и концом и с ограничением по времени его прохождения',
                            ),
                        ],
                        default=0,
                        verbose_name='выбор типа времени мероприятия',
                    ),
                ),
                (
                    'duration',
                    models.PositiveIntegerField(
                        blank=True,
                        help_text='Укажите продолжительность мероприятия в минутах',
                        null=True,
                        verbose_name='продолжительность',
                    ),
                ),
            ],
            options={
                'verbose_name': 'мероприятие',
                'verbose_name_plural': 'мероприятия',
                'ordering': ('category',),
            },
        ),
        migrations.CreateModel(
            name='EventGallery',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        default=None,
                        upload_to=events.models.event_directiry_path,
                        verbose_name='изображение',
                    ),
                ),
            ],
            options={
                'verbose_name': 'фотогалерея',
                'verbose_name_plural': 'фотогалереи',
            },
        ),
        migrations.CreateModel(
            name='EventMainImage',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        default=None,
                        upload_to=events.models.event_directiry_path,
                        verbose_name='изображение',
                    ),
                ),
            ],
            options={
                'verbose_name': 'главное изображение',
                'verbose_name_plural': 'главные изображения',
            },
        ),
        migrations.CreateModel(
            name='EventResults',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'number_of_points',
                    models.PositiveIntegerField(
                        verbose_name='количество набранных баллов'
                    ),
                ),
                (
                    'is_ended',
                    models.BooleanField(
                        default=False,
                        help_text='Завершено ли мероприятие?',
                        verbose_name='завершено',
                    ),
                ),
            ],
            options={
                'verbose_name': 'результат',
                'verbose_name_plural': 'результаты',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='текст поста')),
                (
                    'is_published',
                    models.BooleanField(verbose_name='опубликовано'),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Введите имя тега',
                        max_length=150,
                        verbose_name='имя тега',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=False,
                        help_text='Опубликован тег или нет',
                        verbose_name='опубликован',
                    ),
                ),
            ],
            options={
                'verbose_name': 'тэг',
                'verbose_name_plural': 'тэги',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='текст задания')),
                (
                    'comment',
                    models.TextField(verbose_name='комментарий к заданию'),
                ),
                (
                    'number_of_points',
                    models.PositiveIntegerField(
                        default=1, verbose_name='количество баллов'
                    ),
                ),
                (
                    'task_type',
                    models.IntegerField(
                        choices=[
                            (0, 'тестовое задание'),
                            (1, 'письменное задание'),
                        ],
                        default=0,
                        verbose_name='тип задания',
                    ),
                ),
            ],
            options={
                'verbose_name': 'задание',
                'verbose_name_plural': 'задания',
            },
        ),
        migrations.CreateModel(
            name='TaskImage',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        default=None,
                        upload_to=events.models.task_directiry_path,
                        verbose_name='изображение',
                    ),
                ),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'is_correct',
                    models.BooleanField(verbose_name='правильность ответа'),
                ),
                (
                    'answer',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='events.answer',
                    ),
                ),
            ],
            options={
                'verbose_name': 'ответы пользователя',
            },
        ),
    ]
