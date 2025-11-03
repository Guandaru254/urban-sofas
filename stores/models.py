# stores/models.py (Corrected Indentation)

from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class StoreLocation(models.Model): # No indent
    """ Represents a physical store branch or fulfillment location. """ # 4 spaces
    name = models.CharField( # 4 spaces
        max_length=100,     # 8 spaces (or aligned)
        unique=True,
        help_text="The name of the branch (e.g., Kings Choice - Ngong, Uptown Mall)."
    ) # Closing parenthesis aligned or indented
    slug = models.SlugField( # 4 spaces
        max_length=110,
        unique=True,
        blank=True,
        db_index=True,
        help_text="URL-friendly identifier. Leave blank to auto-generate."
    )
    address_line = models.CharField(max_length=255, blank=True, null=True) # 4 spaces
    area = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Kawangware, Ngong Town, Kitengela") # 4 spaces
    city = models.CharField(max_length=100, default="Nairobi") # 4 spaces
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Branch specific contact number, if any.") # 4 spaces

    simphony_loc_ref = models.CharField( # 4 spaces
        max_length=50,
        unique=True,
        db_index=True,
        blank=True,
        null=True,
        help_text="Simphony Location Reference ID for this branch."
    )
    simphony_rvc_ref = models.CharField( # 4 spaces
        max_length=50,
        db_index=True,
        blank=True,
        null=True,
        help_text="Simphony Revenue Center Reference ID for this branch."
    )
    is_active_online = models.BooleanField( # 4 spaces
        default=True,
        db_index=True,
        help_text="Check if this branch can currently accept and fulfill online orders."
    )

    class Meta: # 4 spaces
        ordering = ['name'] # 8 spaces
        verbose_name = "Store Location"
        verbose_name_plural = "Store Locations"

    def save(self, *args, **kwargs): # 4 spaces
        if not self.slug: # 8 spaces
            self.slug = slugify(f"{self.name}-{self.area}" if self.area else self.name) # 12 spaces
        super().save(*args, **kwargs) # 8 spaces

    def __str__(self): # 4 spaces
        return self.name # 8 spaces