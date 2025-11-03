# menu/urls.py (Updated)

from django.urls import path
from . import views # Import views from the current directory (menu app)

app_name = 'menu' # Define the namespace for this app's URLs

urlpatterns = [
    # Main menu list view (e.g., /menu/)
    # Filtering/sorting uses query parameters like ?category=slug&sort_by=price_asc
    path('', views.menu_list, name='menu_list'),

    # Detail view for a specific menu item (e.g., /menu/item/5/)
    # Using 'item/' prefix for clarity, expects MenuItem ID
    path('item/<int:item_id>/', views.menu_detail, name='menu_detail'),

    # Removed: path('menu_list/', views.menu_list, name='menu_list_page'), # Redundant
    # Removed: path('menu/category/<str:category>/', views.menu_list, name='menu_list_category'), # Incompatible with view logic

    # If you have other menu-specific views (e.g., search results page?), add them here.
    # If your 'home' view truly belongs only to the menu context, you could add it:
    # path('home-test/', views.home, name='menu_home'), # Example if needed
]