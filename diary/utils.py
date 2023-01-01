from functools import wraps
from json import dumps

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django_celery_beat.models import ClockedSchedule, PeriodicTask


def request_teacher(view):
    """decorator for teacher: if user is not a teacher raise error"""

    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.teacher:
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return _view


def request_student(view):
    """decorator for student: only the teacher or
    the owner of this profile can enter else rise error"""

    @wraps(view)
    def _view(request, *args, **kwargs):
        if not (
            request.user.username == kwargs["username"]
            or request.user.is_student == "teacher"
        ):
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return _view


def _get_task_from_database(school_name: str) -> PeriodicTask | None:
    try:
        return PeriodicTask.objects.get(
            name=f"Школа: {school_name}",
        )
    except ObjectDoesNotExist:
        return None


def create_task(name_school, date_end_school_year, school_pk) -> None:
    task = _get_task_from_database(name_school)
    if task:
        return None

    PeriodicTask.objects.create(
        name=f"Школа: {name_school}",
        task="diary.tasks.transition_to_new_school_year",
        clocked=ClockedSchedule.objects.create(clocked_time=date_end_school_year),
        args=dumps((school_pk,)),
        one_off=False,
    )
