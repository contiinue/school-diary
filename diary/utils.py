from functools import wraps

from django.core.exceptions import PermissionDenied


def request_teacher(view):
    """ decorator for teacher: if user is not a teacher raise error """

    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.teacher:
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



