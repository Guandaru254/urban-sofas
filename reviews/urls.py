# reviews/urls.py

from django.urls import path
from . import views

app_name = 'reviews' # <-- ADD THIS LINE!

urlpatterns = [
    # Maps to /reviews/ (when included from main urls.py)
    path('', views.review_list, name='review_list'),        # List all reviews

    # Maps to /reviews/create/
    # Consider if this should be associated with a MenuItem, e.g., /menu/item/<item_id>/review/create/
    path('create/', views.create_review, name='create_review'), # Create a new review

    # Maps to /reviews/<int:pk>/
    path('<int:pk>/', views.review_detail, name='review_detail'), # View review details
]