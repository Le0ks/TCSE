# Generated by Django 4.2 on 2023-12-26 16:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0006_eventresults_is_ended'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='secret_key',
            field=models.CharField(max_length=20, null=True),
        ),
    ]