from functools import wraps

from django.http import HttpResponseRedirect
from django.urls import reverse


def request_teacher(view):
    """decorator for teacher: if user is not a teacher raise error"""

    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.teacher:
            return HttpResponseRedirect(reverse("home"), status=403)
        return view(request, *args, **kwargs)

    return _view


def request_student(view):
    """decorator for student: only the teacher or
    the owner of this profile can enter else rise error"""

    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.student or request.user.teacher:
            return HttpResponseRedirect(reverse("home"), status=403)
        return view(request, *args, **kwargs)

    return _view
