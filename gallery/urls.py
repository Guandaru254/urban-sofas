# gallery/urls.py

from django.urls import path
from .views import gallery_view # Assuming view is named gallery_view

app_name = 'gallery' # <-- ADD THIS LINE!

urlpatterns = [
    # Maps to /gallery/ (when included from main urls.py)
    path('', gallery_view, name='gallery'),
]