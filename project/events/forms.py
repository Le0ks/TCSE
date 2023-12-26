from django.forms import CharField, DateTimeInput, Form, ModelForm

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
            "image",
        )
        widgets = {
            "start_time": DateTimeInput(attrs={"type": "datetime-local"}),
            "finish_time": DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False


class TaskForm(ModelForm):
    tags = CharField(
        max_length=250,
        label="Тэги",
        help_text="Введите тэги через пробел",
    )

    class Meta:
        model = Task
        fields = (
            "text",
            "number_of_points",
            "task_type",
            "tags",
            "comment",
            "image",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False
        self.fields["tags"].required = False
        self.fields["comment"].required = False
        self.fields["task_type"].required = False


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ("text", "is_correct", "comment", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False


class UserAnswerForm(ModelForm):
    class Meta:
        model = UserAnswer
        fields = ("is_correct",)
        labels = {
            "is_correct": "",
        }


class EventConnectionForm(Form):
    secret_key = CharField(
        label="секретный ключ", help_text="Введите секретный ключ мероприятия"
    )
