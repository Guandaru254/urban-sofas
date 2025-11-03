# users/forms.py (Updated)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# *** IMPORTANT: Adjust this import based on where your Profile model lives ***
# If Profile is in 'profiles' app:
from profiles.models import Profile
# If Profile is in the 'users' app (same app as this form):
# from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating users, adding email and phone number fields,
    and ensuring uniqueness checks and Profile creation.
    """
    email = forms.EmailField(
        required=True,
        help_text="Required. Please enter a valid email address."
        # You can add widgets here if needed:
        # widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=15, # Should match Profile.phone_number.max_length
        required=True,
        help_text="Required. Enter phone number (e.g., 07xxxxxxxx or +254...)."
        # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '07...'}),
    )

    class Meta(UserCreationForm.Meta): # Inherit base Meta options (like password help texts)
        model = User
        # Specify fields to be included on the form IN ADDITION to
        # username, password1, password2 which are handled by UserCreationForm
        fields = ("username", "email", "phone_number")

    def clean_email(self):
        """ Ensure the email address is not already taken. """
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists(): # Case-insensitive check
            raise forms.ValidationError(
                "This email address is already in use. Please use a different one."
            )
        return email

    def clean_phone_number(self):
        """ Ensure the phone number is not already registered in a Profile. """
        phone_number = self.cleaned_data.get("phone_number")
        # Add more specific validation for Kenyan phone numbers if desired
        # Example basic check (adjust regex as needed):
        # import re
        # if not re.match(r'^(?:\+?254|0)?(7\d{8})$', phone_number):
        #     raise forms.ValidationError("Please enter a valid Kenyan phone number (e.g., 07xxxxxxxx).")

        # Check uniqueness against Profile model
        # *** Ensure Profile model is imported correctly above ***
        if phone_number and Profile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                "This phone number is already registered. Please use a different one."
            )
        return phone_number

    def save(self, commit=True):
        """
        Save the user instance, set the email, and create the linked Profile.
        """
        user = super().save(commit=False) # Get the User object without saving yet
        user.email = self.cleaned_data["email"] # Set the email from the form

        if commit:
            user.save() # Save the User object
            # Create the Profile object using the saved user and cleaned phone number
            # *** Ensure Profile model is imported correctly above ***
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data["phone_number"]
            )
            # If Profile has other required fields, they must be handled here or have defaults
        return user