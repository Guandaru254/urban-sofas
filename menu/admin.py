# menu/admin.py (Updated for MenuItem, MPTT Category, WITH Brand)

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
# --- Import Category, Brand, and MenuItem ---
from .models import Category, Brand, MenuItem

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """Admin View for Category (using MPTT drag-drop)"""
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    mptt_level_indent = 20

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin View for Brand"""
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(MenuItem) # Register MenuItem
class MenuItemAdmin(admin.ModelAdmin): # Admin for MenuItem
    """Admin View for MenuItem model."""
    list_display = ('name', 'brand', 'category', 'price', 'is_available') # Added brand
    list_filter = ('category', 'brand', 'is_available') # Added brand
    search_fields = ('name', 'description', 'category__name', 'brand__name') # Added brand__name
    list_editable = ('price', 'is_available')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['category', 'brand'] # Added brand
    fieldsets = (
            (None, {'fields': ('name', 'description', 'category', 'brand', 'price', 'image')}), # Added brand
            ('Details', {'fields': ('ingredients', 'dietary_info')}),
            ('Status', {'fields': ('is_available',)}),
            ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)})
        )