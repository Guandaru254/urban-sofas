import json
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
import base64
import requests
import os
from .mpesa_api import get_access_token

def get_access_token():
    """Fetch the access token from M-Pesa Daraja API."""
    consumer_key = os.getenv('MPESA_CONSUMER_KEY')
    consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    response_data = response.json()
    return response_data.get('access_token')

def stk_push(phone_number, amount):
    """Trigger an M-Pesa STK Push request."""
    access_token = get_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}

    # M-Pesa parameters
    business_shortcode = "174379"  # Sandbox shortcode
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    passkey = os.getenv('MPESA_PASSKEY')
    password = base64.b64encode(f"{business_shortcode}{passkey}{timestamp}".encode()).decode()

    payload = {
        "BusinessShortCode": business_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourdomain.com/payments/mpesa-callback/",  # Adjust this for your actual domain
        "AccountReference": "SamakiSamaki",
        "TransactionDesc": "Order Payment"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def mpesa_callback(request):
    """Handle M-Pesa payment response."""
    if request.method == 'POST':
        print(request.body)  # Process and update order status here
        return HttpResponse(status=200)
    
def confirm_order(request):
    """View to handle form submission and trigger STK push for M-Pesa payment."""
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'mpesa':
            phone_number = request.POST.get('mpesa_phone')
            amount = 1000  # Example amount; you should fetch the actual order amount dynamically

            response = stk_push(phone_number, amount)
            if response.get('ResponseCode') == "0":
                return JsonResponse({"message": "STK Push sent successfully. Check your phone to complete the payment."})
            else:
                return JsonResponse({"error": "Failed to initiate payment. Please try again."}, status=400)

        # Add logic for card payments if needed

    return render(request, 'payment.html')