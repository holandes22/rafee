from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        else:
            return request.method in permissions.SAFE_METHODS
