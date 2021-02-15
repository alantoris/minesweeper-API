"""Users views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

#Models
from matches.models import Match

# Permissions
from rest_framework.permissions import IsAuthenticated
from matches.permissions import IsMatchCreator

# Serializers
from matches.serializers import MatchModelSerializer, ClickCellSerializer


class MatchViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Match view set.

    Handle create for a match.
    """
    serializer_class = MatchModelSerializer
    lookup_field = 'uuid'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the match exists."""
        uuid = kwargs['uuid']
        self.match = get_object_or_404(Match, uuid=uuid)
        return super(MatchViewSet, self).dispatch(request, *args, **kwargs)
    
    def get_serializer_context(self):
        """Add match to serializer context."""
        context = super(MatchViewSet, self).get_serializer_context()
        context['match'] = self.match
        return context

    def get_queryset(self):
        filters = { 'creator': self.request.user }
        if self.action == 'click':
            filters['state'] = Match.IN_PROGRESS
        queryset = Match.objects.filter(**filters)
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action == "click":
            permissions.append(IsMatchCreator)
        return [p() for p in permissions]
    
    @action(detail=True, methods=['post'])
    def click(self, request, *args, **kwargs):
        """Change the state of a cell."""
        match = self.get_object()
        serializer = ClickCellSerializer(
            match,
            data=request.data,
            context={'match': match},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        match = serializer.save()
        data = MatchModelSerializer(match).data
        return Response(data, status=status.HTTP_200_OK)

    
