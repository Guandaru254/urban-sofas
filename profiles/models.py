# profiles/models.py (or users/models.py if you placed it there)

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile', # Added related_name for easier access (user.profile)
        primary_key=True # Optional but often good practice for OneToOne linked profile
    )
    phone_number = models.CharField(
        max_length=15, # Keep consistent with your form
        unique=True,   # Ensure phone numbers are unique
        blank=False,   # Required in forms
        null=False,    # Required in the database
        help_text="Phone number (e.g., 07xxxxxxxx or +254...)"
        # default="0700000000" # <-- REMOVED THIS LINE!
    )
    # Optional address fields
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

# Note: If using signals instead of form save for profile creation,
# make sure the signal handler provides a valid phone number.
# For now, we are relying on the form's save method.