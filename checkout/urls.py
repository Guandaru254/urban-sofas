# checkout/urls.py

from django.urls import path
from . import views  # Import views from the checkout app

app_name = 'checkout' # <-- ADD THIS LINE!

urlpatterns = [
    # Maps to /checkout/ (when included with 'checkout/' prefix in main urls.py)
    path('', views.checkout, name='checkout'),

    # You will likely add more URLs here later for different stages
    # of the checkout process, e.g.:
    # path('shipping/', views.shipping_info, name='shipping_info'),
    # path('payment/', views.payment_info, name='payment_info'),
    # path('success/', views.checkout_success, name='checkout_success'),
]