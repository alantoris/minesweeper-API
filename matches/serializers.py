"""Matches serializers."""

# Django
from django.conf import settings

# Django REST Framework
from rest_framework import serializers

# Models
from matches.models import Match


class MatchModelSerializer(serializers.ModelSerializer):
    """Match model serializer."""

    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """Meta class."""

        model = Match
        exclude = ('id', 'board', )

    
    def validate(self, data):
        """Validate.

        Verify that the mines are lower than space avaibles.
        """
        if data['mines'] >= data['width']*data['height']:
            raise serializers.ValidationError("Mines can't be lower than space avaibles ({})".format(
                                                data['width']*data['height'])
                                            )
        return data

    def create(self, data):
        """Create a match."""
        board = Match.create_board(data['width'], data['height'], data['mines'])
        match = Match.objects.create(
            creator=data['creator'],
            board=board
        )
        return match
