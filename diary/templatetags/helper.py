from django import template
from diary.models import *
from datetime import date as now_date
from collections import defaultdict
from datetime import date
import calendar

register = template.Library()
c = calendar.Calendar()


@register.inclusion_tag('diary/get_table.html')
def get_table(value):
    evaluation_and_date = defaultdict(list)
    book = Books.objects.all()
    a = set()
    for i in book:
        ots = i.evaluation_set.filter(student__username=value)
        for elem in ots:
            evaluation_and_date[elem.item.book_name].append((elem.evaluation, elem.date))

    evaluation_and_date.default_factory = None
    for i in c.itermonthdates(date.today().year, date.today().month):
        a.add(i)

    context = {
        'evaluation': evaluation_and_date,
        'date': sorted(a)
    }

    return context


@register.simple_tag()
def get_now_date():
    return now_date.today()




