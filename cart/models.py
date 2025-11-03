# cart/models.py (Corrected to use MenuItem)

from django.db import models
from django.contrib.auth.models import User # Standard Django User model
# --- Import MenuItem from the menu app ---
from menu.models import MenuItem # Use MenuItem, not Product

class Cart(models.Model):
    """
    Represents an item added to a user's shopping cart.
    Each row is a unique combination of a user and a menu item.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items",
        help_text="The user who owns this cart item."
    )
    # --- Link to MenuItem ---
    item = models.ForeignKey(
        MenuItem, # Use MenuItem, not Product
        on_delete=models.CASCADE, # If menu item deleted, remove from carts
        help_text="The menu item added to the cart." # Updated help_text
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Number of this specific item in the cart."
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the item was first added or the entry was created."
    )

    class Meta:
        unique_together = ('user', 'item')
        ordering = ['-added_at']
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def total_price(self):
        """Calculate the total price for this line item (item price * quantity)."""
        if self.item and self.item.price is not None:
             return self.item.price * self.quantity
        return 0

    def __str__(self):
        """String representation of the cart item."""
        # Use try-except for related fields in case they are missing somehow during rendering
        try:
            item_name = self.item.name
            user_name = self.user.username
        except (MenuItem.DoesNotExist, User.DoesNotExist):
            item_name = "[Deleted Item]"
            user_name = "[Deleted User]"
        return f"{self.quantity} x {item_name} for {user_name}"