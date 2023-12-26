from django.contrib.admin import ModelAdmin, register

from .models import Answer, Category, Event, EventResults, Tag, Task


@register(Event)
class EventAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "start_time",
        "is_private",
        "is_ended",
        "is_published",
    )
    list_display_links = ("id",)
    list_editable = ("is_ended", "is_published")
    list_filter = ("is_published",)


@register(EventResults)
class EventResultsAdmin(ModelAdmin):
    list_display = (
        "event",
        "user",
    )
    list_display_links = ("event",)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)


@register(Task)
class TaskAdmin(ModelAdmin):
    list_display = (
        "text",
        "event",
    )
    list_display_links = ("text",)


@register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display = (
        "text",
        "is_correct",
        "task",
    )
    list_editable = ("is_correct",)
    list_display_links = ("text",)
