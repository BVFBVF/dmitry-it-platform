from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class IsMentorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_admin or request.user.is_mentor)
        )


class IsViewerOrAbove(BasePermission):
    """All authenticated users can read."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class EmployeePermission(BasePermission):
    """
    viewer — read only
    mentor — read + create reviews
    admin — full CRUD on employees
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.is_admin


class ReviewPermission(BasePermission):
    """
    viewer — read only
    mentor — read + create
    admin — full access
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        if request.method == 'POST':
            return request.user.is_admin or request.user.is_mentor
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        if request.method in ('PUT', 'PATCH'):
            return request.user.is_admin or request.user.is_mentor
        return request.user.is_admin
