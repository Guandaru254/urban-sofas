# cart/urls.py

from django.urls import path
from . import views # Import views from the current directory (cart app)

app_name = 'cart' # Define the namespace for this app's URLs

urlpatterns = [
    # Display the shopping cart page (e.g., /cart/)
    path('', views.cart_view, name='cart_view'),

    # Add an item to the cart (expects MenuItem ID)
    # e.g., /cart/add/5/
    path('add/<int:item_id>/', views.add_to_cart, name='add_item'), # Using 'add_item' name

    # Remove a specific item entry from the cart (expects Cart object ID)
    # e.g., /cart/remove/12/
    path('remove/<int:cart_item_id>/', views.cart_remove, name='cart_remove'), # Uses cart_item_id

    # Update quantity of an item in the cart (expects MenuItem ID)
    # e.g., /cart/update/5/
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),

    # Clear all items from the cart
    # e.g., /cart/clear/
    path('clear/', views.clear_cart, name='clear_cart'),
]