"""Matches serializers."""

# Django
from django.conf import settings

# Django REST Framework
from rest_framework import serializers

# Models
from matches.models import Match

# Imports
import json


class MatchModelSerializer(serializers.ModelSerializer):
    """Match model serializer."""

    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    board = serializers.SerializerMethodField()

    class Meta:
        """Meta class."""

        model = Match
        exclude = ('id', )
        read_only_fields = ('board',)
    
    def get_board(self, obj):
        return obj.readeable_board()

    
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
    

class ClickCellSerializer(serializers.Serializer):
    """Click cell serializer"""

    row = serializers.IntegerField(min_value=0, required=True)
    col = serializers.IntegerField(min_value=0, required=True)
    state = serializers.CharField()

    def validate(self, data):
        """Verify that the row number and col number are within the limits, and a valid state"""
        match = self.context['match']
        if 'row' in data:
            if data['row'] > match.height:
                raise serializers.ValidationError("Row number cannot be greater than the height of the board  ({})".format(
                                                    match.width)
                                                )
        else:
            raise serializers.ValidationError("The field 'row' is required")

        if 'col' in data:
            if data['col'] > match.height:
                raise serializers.ValidationError("Col number cannot be greater than the width of the board  ({})".format(
                                                    match.height)
                                                )
        else:
            raise serializers.ValidationError("The field 'col' is required")
        
        if 'state' in data:
            if data['state'] not in [Match.FLAGGED, Match.UNKNOWN, Match.DISCOVERED]:
                raise serializers.ValidationError("Invalidad state. Possible values: {} {} {}".format(
                                                Match.FLAGGED, Match.UNKNOWN, Match.DISCOVERED)
                                                )
        else:
            raise serializers.ValidationError("The field 'state' is required")
            
        board = json.loads(match.board)
        if board[data['col']][data['row']]['state'] != Match.UNCLICKED:
            raise serializers.ValidationError("The cell was already discovered")

        return data


    def update(self, instance, data):
        col = data['col']
        row = data['row']
        board = json.loads(instance.board)
        cell = board[col][row]
        if data['state'] == Match.FLAGGED:
            board[col][row]['state'] = Match.FLAGGED
            #TODO: Posibily to count remaining flags
        elif data['state'] == Match.UNKNOWN:
            board[col][row]['state'] = Match.UNKNOWN
        elif data['state'] == Match.DISCOVERED and cell['mined']:
            board[col][row]['state'] = Match.EXPLOITED
            instance.state(Match.FAILED)
        elif data['state'] == Match.DISCOVERED and not cell['mined']:
            board[col][row]['state'] = Match.DISCOVERED
            #TODO: Discover the cell around and set 'number' field into cells
            #TODO: Check if the game is over
        instance.board = json.dumps(board)
        instance.save()
        return instance
