from rest_framework import permissions


class CustomUserOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and obj.id == request.user.id)


class CustomAdmPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser