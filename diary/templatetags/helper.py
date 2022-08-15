from django import template
from diary.models import *

register = template.Library()


@register.inclusion_tag('diary/school_table.html')
def get_user_evaluation():
    user = Students.objects.all()
    context = {
        'user': user,
    }
    return context

