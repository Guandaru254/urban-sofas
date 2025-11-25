# orders/urls.py

from django.urls import path
from . import views

app_name = 'orders' # <-- ADD THIS LINE!n

urlpatterns = [
    # Maps to /orders/ (when included from main urls.py)
    path('', views.order_list, name='order_list'), # List all orders

    # Maps to /orders/orders/create/<int:id>/ (when included from main urls.py)
    # TODO: Review this URL pattern. What does 'id' represent?
    # Order creation usually happens after checkout, not directly like this.
    path('orders/create/<int:id>/', views.create_order, name='create_order'), # Create a new order?

    # Maps to /orders/<int:pk>/ (when included from main urls.py)
    path('<int:pk>/', views.order_detail, name='order_detail'), # View order details
]