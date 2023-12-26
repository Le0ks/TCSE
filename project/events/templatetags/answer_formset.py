from django import template


register = template.Library()


@register.filter(name="get")
def get(dict, num):
    return dict[f"answer-{num}_formset"]


@register.filter(name="concatenate")
def get_number_of_answer(string, number):
    return f"{string}{number}"
