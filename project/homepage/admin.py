from django.contrib.admin import register, ModelAdmin

from .models import New


@register(New)
class EventResultsAdmin(ModelAdmin):
    list_display = ("name", "text", "time")
    list_display_links = ("name",)
