from rest_framework import permissions


class IsTeacherPermissions(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return not request.user.student
