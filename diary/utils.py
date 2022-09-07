from functools import wraps
from django.core.exceptions import PermissionDenied


def request_teacher(view):
    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.is_student == 'teacher':
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def request_student(view):
    @wraps(view)
    def _view(request, *args, **kwargs):
        print(request.user.is_staff)
        if not (request.user.username == kwargs['username'] or
                request.user.is_student == 'teacher'):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view