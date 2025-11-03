# payments/urls.py

from django.urls import path
from . import views

app_name = 'payments' # <-- ADD THIS LINE!

urlpatterns = [
    # Endpoint to initiate the STK Push request
    path('stk-push/', views.stk_push, name='stk_push'),

    # Endpoint possibly used after payment attempt or confirmation page
    path('confirm-order/', views.confirm_order, name='confirm_order'),

    # Endpoint to receive asynchronous callback from M-Pesa API
    # Ensure this URL is accessible externally by the M-Pesa API
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
]