from datetime import datetime
from django.shortcuts import get_object_or_404
from diary.models import Evaluation, Quarter, MyUser


def get_evaluation(student, quarter: Quarter, item) -> list[Evaluation]:
    return Evaluation.objects.filter(
        date__range=(quarter.start, quarter.end), student=student, item__book_name=item
    )


def get_now_quarter(quarter: int | bool = False) -> Quarter:
    if quarter is False:
        now = datetime.today().date()
        return get_object_or_404(Quarter, start__lte=now, end__gte=now)

    return get_object_or_404(Quarter, pk=quarter)


def get_evaluation_of_quarter(
    student: MyUser, item: str, quarter: int | bool = False
) -> list[Evaluation]:
    quarter = get_now_quarter(quarter)
    return get_evaluation(student, quarter, item)
