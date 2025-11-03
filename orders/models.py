# orders/models.py (Corrected Version)

from django.db import models
from django.contrib.auth.models import User
# --- Import MenuItem from menu app ---
from menu.models import MenuItem
from decimal import Decimal # Import Decimal

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('card', 'Debit/Credit Card'),
        ('cash_on_delivery', 'Cash on Delivery'), # Added Option
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Out_for_Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders') # Use SET_NULL, related_name 'orders'
    # Store address/contact details directly on order
    customer_name = models.CharField(max_length=100, help_text="Name used for the order")
    customer_phone = models.CharField(max_length=15, help_text="Phone number used for the order")
    delivery_address = models.TextField(help_text="Full delivery address") # Make required? Depends on if you allow pickup
    delivery_city = models.CharField(max_length=100, blank=True, null=True)
    delivery_postal_code = models.CharField(max_length=20, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)

    # Store calculated totals and payment method at time of order
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) # Store fee used, default 0
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) # Grand total stored

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True) # Allow selection
    # payment_status = models.CharField(max_length=20, default='Pending') # Optional
    # payment_transaction_id = models.CharField(max_length=100, blank=True, null=True) # Optional

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user.username if self.user else 'Guest'} on {self.created_at.strftime('%Y-%m-%d')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # --- Link to MenuItem using 'menu_item' field name ---
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.SET_NULL, # Keep order item history if menu item deleted
        related_name='order_items',
        null=True, # Required if using SET_NULL
        blank=False # An order item must link to a menu item (even if null later)
    )
    # --- Store price AT TIME OF ORDER ---
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    # --- Calculate total based on STORED price ---
    @property
    def total_price(self):
        """Calculate total price for this specific order item."""
        if self.price_per_unit is not None and self.quantity is not None:
             return self.price_per_unit * self.quantity
        return 0

    def __str__(self):
        # --- Use correct field name 'menu_item' ---
        item_name = self.menu_item.name if self.menu_item else "[Deleted Menu Item]"
        return f"{self.quantity} x {item_name} (Order #{self.order.id})"