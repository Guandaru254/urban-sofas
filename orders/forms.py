from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'special_instructions']  # Removed 'menu_items'
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'special_instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special instructions?',
                'rows': 4
            }),
        }
        labels = {
            'customer_name': 'Name',
            'customer_phone': 'Phone Number',
            'special_instructions': 'Special Instructions',
        }