"""Main URLs module."""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('matches.urls', 'matches'), namespace='matches')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)