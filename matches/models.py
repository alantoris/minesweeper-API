"""Matchs models."""

# Django
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from utils.models import BaseModel

# Models
from django.contrib.auth.models import User

#Imports
import json
import numpy as np
import uuid


class Match(BaseModel):
    """Match model.

    Match represent a particular game
    """

    IN_PROGRESS = 'IP'
    SUCCESSFUL = 'SC'
    FAILED = 'FA'
    STATE_CHOICES = ((IN_PROGRESS, "In progress"), (SUCCESSFUL, "Successful"), (FAILED, "Failed"))

    UNCLICKED = 'UNC'
    FLAGGED = 'FLG'
    UNKNOWN = 'UNK'
    DISCOVERED = 'DIS'
    EXPLOITED = 'EXP'

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) 
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=IN_PROGRESS)
    board = models.JSONField(null=True, blank=True)
    mines = models.PositiveIntegerField()
    width = models.PositiveIntegerField(
        validators=[MinValueValidator(settings.BOARD_MIN_WIDTH), MaxValueValidator(settings.BOARD_MAX_WIDTH)])
    height = models.PositiveIntegerField(
        validators=[MinValueValidator(settings.BOARD_MIN_HEIGHT), MaxValueValidator(settings.BOARD_MAX_HEIGHT)])
    remaining_flags = models.PositiveIntegerField()
    remaining_free_cells = models.PositiveIntegerField()
    
    def __str__(self):
        return "{}: {}".format(self.uuid, self.state)

    @classmethod
    def create_board(cls, 
                    width=settings.BOARD_WIDTH_DEFAULT, 
                    height=settings.BOARD_HEIGHT_DEFAULT, 
                    mines=settings.BOARD_MINES_DEFAULT):
        rng = np.random.default_rng()
        random_index = rng.choice(width*height, size=mines, replace=False)
        board = []
        index = 0
        for i in range(height):
            row = []
            for j in range(width):
                row.append({
                    'mined': index in random_index,
                    'state': cls.UNCLICKED,
                    'number': None
                }) 
                index = index + 1
            board.append(row)
        return json.dumps(board)
    
    def readeable_board(self):
        board = json.loads(self.board)
        for x in board:
            for y in x:
                y.pop('mined')
        return board
    
    def discover_around(self, board, col, row, checked_cells=[], cells_discovered=0):
        """Recursively discover cells to free """
        board[col][row]['state'] = Match.DISCOVERED
        cells_discovered = cells_discovered + 1
        around_coordinates = []
        mines_around = 0
        for c in range(col - 1, col + 2):
            if c < 0 or c >= self.width:
                continue
            for r in range(row - 1, row + 2):
                if (r < 0 or r >= self.height) or ((c,r) in checked_cells) or (c == col and r == row):
                    continue
                if board[c][r]['mined']:
                    mines_around = mines_around + 1
                else:
                    around_coordinates.append((c,r))
        if mines_around > 0:
            board[col][row]['number'] = mines_around
            return board, checked_cells, cells_discovered
        else:
            already_checked = around_coordinates + checked_cells + [(col,row)]
            for cell in around_coordinates:
                board, already_checked, cells_discovered = self.discover_around(board, cell[0], cell[1], already_checked, cells_discovered)
            return board, already_checked, cells_discovered
