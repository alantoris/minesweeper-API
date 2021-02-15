"""Users URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import MatchViewSet

router = DefaultRouter()
router.register(r'matches', MatchViewSet, basename='matches')

urlpatterns = [
    path('', include(router.urls))
]