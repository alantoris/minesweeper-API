"""Matches permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsMatchCreator(BasePermission):
    """Verify requesting user is the match creator."""

    def has_object_permission(self, request, view, obj):
        """Verify requesting user is the match creator."""
        return request.user == obj.creator