# orders/admin.py (Enhanced Version - Optional)

from django.contrib import admin
from .models import Order, OrderItem

# Define an inline admin descriptor for OrderItem
class OrderItemInline(admin.TabularInline): # TabularInline shows items in a table
    model = OrderItem
    # Fields to display/edit within the Order page
    fields = ('menu_item', 'price_per_unit', 'quantity', 'total_price')
    readonly_fields = ('menu_item', 'price_per_unit', 'total_price') # Make some fields read-only here
    extra = 0 # Don't show extra blank rows for adding new items here
    can_delete = False # Usually don't delete items directly from order admin

    # Define the total_price method for display
    def total_price(self, obj):
        return obj.total_price() # Call the model method
    total_price.short_description = 'Line Total' # Column header


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Customized Admin for Order model """
    list_display = (
        'id', 'user', 'customer_name', 'status', 'total_price', 'created_at'
    ) # Columns shown in the order list view
    list_filter = ('status', 'created_at', 'payment_method') # Filters available in the sidebar
    search_fields = (
        'id', 'user__username', 'customer_name', 'customer_phone', 'items__menu_item__name'
    ) # Allow searching by these fields
    list_display_links = ('id', 'user', 'customer_name') # Make these fields clickable links
    readonly_fields = (
        'user', 'subtotal', 'delivery_fee', 'total_price',
        'created_at', 'updated_at', 'payment_method', # Make key fields read-only after creation
        'customer_name', 'customer_phone', 'delivery_address', # Snapshot data
        'delivery_city', 'delivery_postal_code', 'special_instructions',
    )
    # Include the OrderItemInline to show items within the Order detail page
    inlines = [OrderItemInline]

    # Optionally organize fields further with fieldsets
    fieldsets = (
        ('Order Information', {'fields': ('id', 'user', 'status', 'created_at', 'updated_at')}),
        ('Amount Details', {'fields': ('subtotal', 'delivery_fee', 'total_price')}),
        ('Payment Details', {'fields': ('payment_method',)}), # Add payment_status, transaction_id if used
        ('Customer & Delivery', {'fields': ('customer_name', 'customer_phone', 'delivery_address', 'delivery_city', 'delivery_postal_code', 'special_instructions')}),
    )

    # Add id to readonly_fields if using fieldsets that include it
    readonly_fields = ('id',) + readonly_fields


# Note: Don't need admin.site.register(OrderItem) separately if using inline
# admin.site.register(Order) # Don't need this if using @admin.register decorator