# menu/admin.py (Cleaned & Optimized for Restaurant Site)

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Brand, MenuItem


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """Admin View for Category (MPTT tree view)"""
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


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin View for Menu Items (Restaurant Menu Management)"""
    list_display = ('name', 'brand', 'category', 'price', 'is_available')
    list_filter = ('category', 'brand', 'is_available')
    search_fields = ('name', 'description', 'category__name', 'brand__name')
    list_editable = ('price', 'is_available')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['category', 'brand']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'category', 'brand', 'price', 'image')
        }),
        ('Status', {
            'fields': ('is_available',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    ordering = ('category', 'name')
