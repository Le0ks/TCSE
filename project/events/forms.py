from django.forms import (
    ModelForm,
    DateTimeInput,
    CharField,
)

from .models import Answer, Event, Task, UserAnswer


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = (
            "name",
            "description",
            "answer_rule",
            "type_by_time",
            "start_time",
            "finish_time",
            "duration",
            "is_private",
        )
        widgets = {
            "start_time": DateTimeInput(attrs={"type": "datetime-local"}),
            "finish_time": DateTimeInput(attrs={"type": "datetime-local"}),
        }


class TaskForm(ModelForm):
    tags = CharField(
        max_length=250,
        label="Тэги",
        help_text="Введите тэги через пробел (например: #tag1 #tag2 #tag3 #tag4 #tag5)",
    )

    class Meta:
        model = Task
        fields = ("text",)


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = (
            "text",
            "is_correct",
        )


class UserAnswerForm(ModelForm):
    class Meta:
        model = UserAnswer
        fields = ("is_correct",)
        labels = {
            "is_correct": "",
        }
