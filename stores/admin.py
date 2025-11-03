# stores/admin.py

from django.contrib import admin
from .models import StoreLocation # Import your StoreLocation model

@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    """ Admin configuration for Store Locations """
    list_display = (
        'name',
        'area',
        'city',
        'simphony_loc_ref', # Show Simphony IDs in list
        'simphony_rvc_ref',
        'is_active_online', # Show if it accepts online orders
        'phone_number'
        )
    list_filter = ('is_active_online', 'city', 'area') # Allow filtering by status/location
    search_fields = ('name', 'area', 'city', 'simphony_loc_ref', 'simphony_rvc_ref') # Allow searching
    prepopulated_fields = {'slug': ('name',)} # Auto-fill slug from name
    list_editable = ('is_active_online',) # Allow quick toggling of online status

    fieldsets = ( # Organize the edit form
        (None, {
            'fields': ('name', 'slug', 'is_active_online')
        }),
        ('Location & Contact', {
            'fields': ('address_line', 'area', 'city', 'phone_number')
        }),
        ('POS Integration (Optional for Demo)', {
            'fields': ('simphony_loc_ref', 'simphony_rvc_ref'),
            'classes': ('collapse',), # Keep collapsed initially if IDs aren't ready
            'description': "Enter the exact Location and Revenue Center IDs from Oracle Simphony POS for this branch."
        }),
    )