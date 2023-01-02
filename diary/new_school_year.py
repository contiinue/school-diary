from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta, datetime

from django_celery_beat.models import PeriodicTask, ClockedSchedule

from .models import SchoolClass, Quarter, School, StudentRegistration


def get_timedelta_year() -> timedelta:
    if datetime.now().year % 4 != 0:
        return timedelta(days=365)
    return timedelta(days=366)


def update_task(end_school_year, name_school: str):
    """Update task for transition to the new school year."""
    time_to_start_task = ClockedSchedule.objects.create(
        clocked_time=end_school_year + get_timedelta_year()
    )
    task = PeriodicTask.objects.get(name=f"Школа: {name_school}")
    task.clocked = time_to_start_task
    task.one_off = True
    task.save()


def _get_student_class(
    number_class: int, name_class: str, school: School
) -> SchoolClass | None:
    """Get student-class for change his at student."""
    try:
        if number_class > 11:
            return None

        return SchoolClass.objects.select_related("school").get(
            number_class=number_class, name_class=name_class, school=school
        )
    except ObjectDoesNotExist:
        return None


def switch_to_a_new_class(school: School) -> None:
    """Transferring a school class to +1. If class > 11 will change student is_is_alum to True."""
    students = StudentRegistration.objects.select_related("learned_class").filter(
        learned_class__school=school, is_alum=False
    )
    for student in students:
        new_school_class = _get_student_class(
            student.learned_class.number_class + 1,
            student.learned_class.name_class,
            school,
        )
        if new_school_class:
            student.learned_class = new_school_class
        else:
            student.is_alum = True
        student.save()


def switch_to_a_new_quarter(school: School) -> None:
    """Clone school quarters last year and +365 days to their date"""
    year = get_timedelta_year()
    for quarter in Quarter.objects.select_related("school").filter(
        school=school, start__range=(school.start_school_year, school.end_school_year)
    ):
        q = Quarter.objects.create(
            name=quarter.name,
            start=quarter.start + year,
            end=quarter.end + year,
            school=quarter.school,
        )
        q.save()


def switch_to_a_new_school_year_time_zone(school: School) -> School:
    year: timedelta = get_timedelta_year()
    school.start_school_year += year
    school.end_school_year += year
    school.save()
    return school


def transition_to_the_new_school_year(school_id: int) -> None:
    school = School.objects.get(pk=school_id)
    switch_to_a_new_class(school)
    switch_to_a_new_quarter(school)
    update_school_year = switch_to_a_new_school_year_time_zone(school)
    update_task(
        update_school_year.end_school_year,
        update_school_year.name_school,
    )
