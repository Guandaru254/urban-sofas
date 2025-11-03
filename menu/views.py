# menu/views.py (Updated menu_detail to fetch related items)

from django.shortcuts import render, get_object_or_404
# --- Import models correctly ---
from .models import MenuItem, Category # Use MenuItem consistently
from django.db.models import Q # For potential complex searches later
from django.contrib import messages # If you want to add messages here

# NOTE: Cart count logic is here for now, consider a context processor later
# from cart.models import Cart

# --- Menu List View (Keep as is from your last version) ---
def menu_list(request):
    """ Displays the list of available menu items, with filtering and sorting. """
    categories = Category.objects.all() # Get all categories for display

    # --- Get filter/sort parameters ---
    selected_category_slug = request.GET.get('category', None)
    search_query = request.GET.get('search', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    sort_by = request.GET.get('sort_by', None)
    # --- Cart Item Count --- (Example logic)
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            from cart.models import Cart # Import where needed or globally
            cart_items = Cart.objects.filter(user=request.user)
            cart_item_count = sum(item.quantity for item in cart_items)
        except (ImportError, AttributeError, Cart.DoesNotExist):
             pass # Handle gracefully

    # --- Filtering ---
    menu_items = MenuItem.objects.filter(is_available=True).select_related('category')

    if selected_category_slug:
        try:
            selected_category = Category.objects.get(slug=selected_category_slug)
            descendant_categories = selected_category.get_descendants(include_self=True)
            menu_items = menu_items.filter(category__in=descendant_categories)
        except Category.DoesNotExist:
            messages.warning(request, "Selected category not found.")

    if search_query:
        menu_items = menu_items.filter(name__icontains=search_query)

    try: # Price filtering
        if min_price is not None and min_price != '':
            menu_items = menu_items.filter(price__gte=float(min_price))
        if max_price is not None and max_price != '':
            menu_items = menu_items.filter(price__lte=float(max_price))
    except (ValueError, TypeError):
        messages.warning(request, "Invalid price value entered.")
        pass

    # --- Sorting ---
    valid_sort_fields = {
        'price_asc': 'price', 'price_desc': '-price',
        'name_asc': 'name', 'name_desc': '-name',
    }
    sort_field = valid_sort_fields.get(sort_by)
    if sort_field:
        menu_items = menu_items.order_by(sort_field)

    # --- Prepare Context for Template ---
    context = {
        'menu_items': menu_items,
        'categories': categories,
        'cart_item_count': cart_item_count,
        'selected_category_slug': selected_category_slug,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }

    return render(request, 'menu/menu_list.html', context) # Assumes template is menu/menu_list.html


# --- Menu Detail View (UPDATED) ---
def menu_detail(request, item_id):
    """ Displays details for a specific, available menu item
        and fetches related items from the same category.
    """
    # Fetch the main item, prefetch related category/brand for efficiency
    menu_item = get_object_or_404(
        MenuItem.objects.select_related('category', 'brand'), # Added brand preload
        pk=item_id, # Use pk consistently
        is_available=True
    )

    # --- ADDED: Fetch Related Items ---
    related_items = None
    if menu_item.category: # Check if the item has a category
        related_items = MenuItem.objects.filter(
            category=menu_item.category,   # Find items in the same category
            is_available=True
        ).exclude(
            pk=menu_item.pk                # Exclude the current item itself
        ).select_related('category')[0:3] # Limit to 3 items, preload category
    # --- END: Fetch Related Items ---

    # Cart Count Logic
    cart_item_count = 0
    if request.user.is_authenticated:
         try:
             from cart.models import Cart
             cart_items = Cart.objects.filter(user=request.user)
             cart_item_count = sum(item.quantity for item in cart_items)
         except (ImportError, AttributeError, Cart.DoesNotExist):
             pass

    context = {
        'item': menu_item,
        'related_items': related_items, # <-- Add related items to context
        'cart_item_count': cart_item_count,
    }
    # Ensure this template path is correct for your detail page
    return render(request, 'menu/menu_detail.html', context)


# --- Home View ---
# Keep this if needed, ensure it's mapped correctly in main urls.py if not using TemplateView
def home(request):
    """ Renders the home page. """
    context = {}
    return render(request, 'home.html', context)