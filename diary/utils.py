from functools import wraps
from typing import Union, Literal

from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from diary.forms import StudentRegistrationForm, TeacherRegistrationForm, MyUserForm
from diary.models import StudentRegistration, TeacherRegistration, MyUser


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


def check_is_valid_form(form: TeacherRegistrationForm | StudentRegistrationForm) -> \
        Union[StudentRegistrationForm, TeacherRegistrationForm, TeacherRegistration, StudentRegistration]:
    if form.is_valid():
        return form.save(commit=False)
    return form


def get_teacher_or_student_form(
        post: dict) -> tuple[TeacherRegistration, str] | tuple[StudentRegistration, str]:
    if 'item' in post:
        return check_is_valid_form(
            StudentRegistrationForm(post)
        ), 'teacher'

    if 'learned_class' in post:
        return check_is_valid_form(
            StudentRegistrationForm(post)
        ), 'student'


def _do_save_user_to_model(
        user_form: MyUser, register: Union[StudentRegistrationForm, TeacherRegistrationForm]) -> MyUserForm:
    u = user_form.save(commit=False)
    register.save()
    if isinstance(register, StudentRegistration):
        u.student = register
        u.save()
        return u
    u.teacher = register
    u.save()
    return u


def save_user_to_model(request, register: Union[StudentRegistrationForm, TeacherRegistrationForm]):
    form = MyUserForm(request.POST)
    if form.is_valid():
        return _do_save_user_to_model(form, register)
    return form


