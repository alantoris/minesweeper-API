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
    mines = models.PositiveIntegerField(default=settings.BOARD_MINES_DEFAULT)
    width = models.PositiveIntegerField(
        default=settings.BOARD_WIDTH_DEFAULT, 
        validators=[MinValueValidator(settings.BOARD_MIN_WIDTH), MaxValueValidator(settings.BOARD_MAX_WIDTH)])
    height = models.PositiveIntegerField(
        default=settings.BOARD_HEIGHT_DEFAULT, 
        validators=[MinValueValidator(settings.BOARD_MIN_HEIGHT), MaxValueValidator(settings.BOARD_MAX_HEIGHT)])
    
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
                    'numer': None
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
