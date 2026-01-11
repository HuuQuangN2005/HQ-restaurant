from rest_framework import permissions
from users.models import UserType


class IsVerifiedCookerOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == UserType.ADMIN:
            return True

        if request.user.role == UserType.COOKER:
            return getattr(request.user, "is_approved", False)

        return False


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff:
            return True

        return False
