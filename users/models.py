# users/models.py

from django.contrib.auth.models import User
from django.db import models

# DELETE THE ENTIRE CLASS BELOW THIS LINE
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=15, unique=True, blank=False, null=False, default="0700000000") # Updated
#     address = models.TextField(blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     postal_code = models.CharField(max_length=20, blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.user.username} Profile"

# Keep any OTHER models you might have defined in users/models.py below here,
# but if Profile was the only one, this file might become empty (which is okay).