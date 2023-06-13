from rest_framework import permissions

from userprofile.models.userprofile import RoleChoices


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == RoleChoices.ADMIN
        except:
            return False


class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == RoleChoices.VENDOR
        except:
            return False


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == RoleChoices.USER
        except:
            return False



