from django import template
from datetime import date

register = template.Library()


@register.filter()
def to_evaluation_list(evaluations):
    return [i.evaluation for i in evaluations]


@register.simple_tag()
def get_now_date():
    return date.today()


@register.filter()
def middle_eval(evaluations: list):
    try:
        return round(sum(evaluations) / len(evaluations), 2)
    except ZeroDivisionError:
        return 0
