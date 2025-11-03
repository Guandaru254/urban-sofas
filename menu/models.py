# menu/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

# --- Category Model (e.g., "Sofa", "Chair", "Table") ---
class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True, db_index=True, help_text="e.g., 'Sofa Sets', 'Dining Tables'")
    slug = models.SlugField(max_length=110, unique=True, blank=True, db_index=True, help_text="URL-friendly version. Auto-generated.")
    parent = TreeForeignKey(
        'self', on_delete=models.PROTECT, null=True, blank=True,
        related_name='children', db_index=True, help_text="Select parent for sub-categories. e.g., '3-Seater' under 'Sofa Sets'."
    )
    description = models.TextField(blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"{reverse('menu:menu_list')}?category={self.slug}"

    def __str__(self):
        return self.name

# --- Brand Model (e.g., "La-Z-Boy", "Ashley Furniture") ---
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

# --- MenuItem Model (Keeping the original name) ---
class MenuItem(models.Model):  # Keep this name
    name = models.CharField(max_length=255, db_index=True, help_text="e.g., 'Modern Velvet Sofa'")
    description = models.TextField(help_text="Detailed description, dimensions, and materials.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in KES")
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True) # Keep original upload path
    
    category = TreeForeignKey(
        Category,
        related_name='menu_items', # Keep original related_name
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    
    brand = models.ForeignKey(
        Brand,
        related_name='menu_items', # Keep original related_name
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True
    )
    
    # You can add or keep these furniture-specific fields
    dimensions = models.CharField(max_length=200, blank=True, null=True, help_text="e.g., 'W: 85in, H: 30in, D: 34in'")
    material = models.CharField(max_length=200, blank=True, null=True, help_text="e.g., 'Velvet Fabric, Solid Wood'")

    is_available = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def get_absolute_url(self):
        return reverse('menu:menu_detail', kwargs={'item_id': self.pk})

    def __str__(self):
        return self.name