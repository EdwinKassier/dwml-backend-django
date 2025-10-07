"""Custom permissions for the API."""

from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to modify data,
    but allow read-only access for unauthenticated users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed for authenticated users
        return request.user and request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to modify data,
    but allow read-only access for all users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed for admin users
        return request.user and request.user.is_staff
