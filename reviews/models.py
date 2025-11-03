# reviews/models.py (Corrected)

from django.db import models
# --- Import MenuItem from menu app ---
from menu.models import MenuItem
from django.contrib.auth.models import User
# --- Import validators for rating ---
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    """ Represents a customer review for a specific menu item. """
    # --- Link to MenuItem ---
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE, # If item deleted, delete review
        related_name='reviews' # Access via menu_item.reviews.all()
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # If user deleted, delete review
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        # --- Add validation for 1-5 stars ---
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating (1 to 5 stars)"
    )
    comment = models.TextField(
        blank=True, # Allow reviews with just a rating
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # Optional: Add for moderation
    # is_approved = models.BooleanField(default=False, db_index=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # --- Prevent multiple reviews by same user for same item ---
        unique_together = ('user', 'menu_item')
        ordering = ['-created_at'] # Show newest reviews first
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        # --- Use correct field name ---
        item_name = self.menu_item.name if self.menu_item else "[Deleted Item]"
        return f"Review for {item_name} by {self.user.username} ({self.rating} Stars)"