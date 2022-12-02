from rest_framework import permissions


class IsTeacherPermissions(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        """ if user is teacher return True else False """
        return not request.user.student
