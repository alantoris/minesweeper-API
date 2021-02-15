"""Users views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action

#Models
from matches.models import Match

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from matches.serializers import MatchModelSerializer


class MatchViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Match view set.

    Handle create for a match.
    """
    serializer_class = MatchModelSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user
        queryset = Match.objects.filter(creator=user)
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    
