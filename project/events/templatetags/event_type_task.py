from django import template

register = template.Library()


@register.filter(name="get_url_for_task_category")
def get_url_for_task_category(category):
    return f"events:event_{category}_task"
