from functools import wraps
from typing import Union, Literal
from django.core.exceptions import PermissionDenied
from diary.forms import StudentRegistrationForm, TeacherRegistrationForm


def request_teacher(view):
    """ decorator for teacher: if user is not a teacher raise error """

    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.is_student == 'teacher':
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return _view


def request_student(view):
    """ decorator for student: only the teacher or
    the owner of this profile can enter else rise error """

    @wraps(view)
    def _view(request, *args, **kwargs):
        if not (request.user.username == kwargs['username'] or
                request.user.is_student == 'teacher'):
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return _view


def check_is_valid_form(
        form: TeacherRegistrationForm | StudentRegistrationForm) -> TeacherRegistrationForm | StudentRegistrationForm:
    if form.is_valid():
        return form.save(commit=True)


def get_teacher_or_student_form(
        post: dict) -> tuple[TeacherRegistrationForm, str] | tuple[StudentRegistrationForm, str]:
    if 'item' in post:
        return check_is_valid_form(
            StudentRegistrationForm(post)
        ), 'teacher'

    if 'learned_class' in post:
        return check_is_valid_form(
            StudentRegistrationForm(post)
        ), 'student'


def save_user_to_model(request, user):
    u = user.save(commit=False)
    if isinstance(register, StudentRegistration):
        u.student = register
        u.save()
        login(request, u)