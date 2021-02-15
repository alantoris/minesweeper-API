"""Matches admin."""

# Django
from django.contrib import admin

# Models
from matches.models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Match admin."""

    list_display = (
        'uuid',
        'creator',
        'state',
    )
    search_fields = ('creator', 'state')
    list_filter = (
        'state',
    )
