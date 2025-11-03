from django import forms

class CheckoutForm(forms.Form):
    special_instructions = forms.CharField(widget=forms.Textarea, required=False)
    delivery_address = forms.CharField(widget=forms.Textarea, required=True)
    delivery_city = forms.CharField(max_length=100, required=True)
    delivery_postal_code = forms.CharField(max_length=10, required=False)
    mpesa_number = forms.CharField(max_length=15, required=True)  # For M-Pesa payment