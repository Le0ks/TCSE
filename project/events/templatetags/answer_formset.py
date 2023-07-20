from django import template

register = template.Library()


@register.filter(name="get")
def get(dict, num):
    return dict[f"answer-{num}_formset"]
