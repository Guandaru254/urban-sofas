# profiles/urls.py

from django.urls import path
from . import views

app_name = 'profiles' # <-- ADD THIS LINE!

urlpatterns = [
    # Maps to /profile/ (when included with 'profile/' prefix in main urls.py)
    path('', views.profile, name='profile'), # Profile view at the app's root

    # Maps to /profile/update/ (when included with 'profile/' prefix)
    path('update/', views.update_profile, name='update_profile'), # Update profile view
]