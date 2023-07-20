# Generated by Django 4.2 on 2023-05-17 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventresults",
            name="is_ended",
            field=models.BooleanField(
                default=False,
                help_text="Завершено ли мероприятие?",
                verbose_name="завершено",
            ),
        ),
        migrations.AlterField(
            model_name="answer",
            name="comment",
            field=models.TextField(
                blank=True, null=True, verbose_name="комментарий к ответу"
            ),
        ),
        migrations.AlterField(
            model_name="useranswer",
            name="answer",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.answer",
            ),
        ),
        migrations.AlterField(
            model_name="useranswer",
            name="user",
            field=models.ForeignKey(
                help_text="пользователь, который дал ответ",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_answers",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
    ]
