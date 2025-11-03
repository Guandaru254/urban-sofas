# cart/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.urls import reverse
from .models import Cart
from menu.models import MenuItem # Import MenuItem from the menu app

# -----------------------------
# View Cart
# -----------------------------
@login_required
def cart_view(request):
    """ Displays the user's shopping cart contents. """
    cart_items = Cart.objects.filter(user=request.user).select_related('item', 'item__category') # Optimize query
    
    # Calculate subtotal safely using the model method
    subtotal = sum(item.total_price() for item in cart_items if hasattr(item, 'total_price'))
    
    # Consider making delivery fee dynamic (e.g., settings, location based)
    delivery_fee = 200
    total_price = subtotal + delivery_fee

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total_price': total_price
    }
    return render(request, 'cart/cart.html', context)

# -----------------------------
# Add Item to Cart
# -----------------------------
@login_required
def add_to_cart(request, item_id):
    """ Adds a MenuItem to the cart or increments its quantity.
        Handles both standard POST/GET requests (redirects) and AJAX requests (returns JSON).
    """
    # Allow GET for simplicity via links/buttons, but POST is semantically better for actions
    # if request.method != 'POST':
    #     return HttpResponseBadRequest("POST method required.")

    menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True) # Ensure item exists and is available
    quantity_to_add = 1 # Default quantity

    # Optional: Handle quantity if submitted via standard form POST
    # is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    # if request.method == 'POST' and not is_ajax:
    #     try:
    #         quantity_from_post = int(request.POST.get('quantity', 1))
    #         if quantity_from_post >= 1:
    #             quantity_to_add = quantity_from_post
    #     except (ValueError, TypeError):
    #         messages.error(request, "Invalid quantity submitted.")
    #         return redirect(request.META.get('HTTP_REFERER', reverse('menu:menu_list'))) # Redirect back

    # Get or create cart item using the unique_together constraint
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        item=menu_item,
        defaults={'quantity': 0} # Start quantity at 0 if creating
    )

    # Increment quantity and save
    cart_item.quantity += quantity_to_add
    cart_item.save()

    # --- Differentiate response based on request type ---
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax:
        # Calculate current cart count (distinct items or total quantity)
        # cart_item_count = Cart.objects.filter(user=request.user).count() # Count distinct items
        total_quantity = sum(item.quantity for item in Cart.objects.filter(user=request.user)) # Sum all quantities

        return JsonResponse({
            'status': 'success',
            'message': f"'{menu_item.name}' added to cart.",
            'cart_item_count': total_quantity # Send total quantity back
        })
    else:
        # Standard request: Add message and redirect
        messages.success(request, f"'{menu_item.name}' added to cart.")
        # Redirect back to the previous page or a default (like menu list)
        # return redirect(request.META.get('HTTP_REFERER', reverse('menu:menu_list')))
        return redirect('menu:menu_list') # Or redirect('cart:cart_view')

# -----------------------------
# Remove Item from Cart
# -----------------------------
@login_required
def cart_remove(request, cart_item_id): # Expects Cart item's ID
    """ Removes a specific item entry from the user's cart. """
    # POST is safer for deletion actions
    # if request.method != 'POST':
    #    return HttpResponseBadRequest("POST method required.")

    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user) # Find specific cart row by its ID
    item_name = cart_item.item.name # Get name for message before deleting
    cart_item.delete()

    messages.success(request, f"'{item_name}' removed from your cart.")
    return redirect('cart:cart_view') # Redirect back to cart


# -----------------------------
# Update Cart Item Quantity
# -----------------------------
@login_required
def update_cart(request, item_id): # Expects MenuItem ID
    """ Updates the quantity of an item in the cart via AJAX POST request. """
    if request.method != 'POST':
       return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if not is_ajax:
         return JsonResponse({'status': 'error', 'message': 'AJAX request required.'}, status=400)

    try:
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity < 0: # Cannot have negative quantity
             raise ValueError("Quantity cannot be negative.")

        # Find the cart item based on user and MenuItem ID
        cart_item = get_object_or_404(Cart, user=request.user, item__id=item_id)

        item_total = 0
        removed = False
        if new_quantity == 0:
            # Remove item if quantity is set to 0
            cart_item.delete()
            removed = True
        else:
            # Update quantity
            cart_item.quantity = new_quantity
            cart_item.save()
            item_total = cart_item.total_price()

        # Recalculate overall cart totals
        cart_items = Cart.objects.filter(user=request.user)
        subtotal = sum(item.total_price() for item in cart_items if hasattr(item, 'total_price'))
        delivery_fee = 200 # Make dynamic later
        total_price = subtotal + delivery_fee
        # cart_item_count = cart_items.count() # Distinct items
        total_quantity = sum(item.quantity for item in cart_items) # Sum of quantities

        return JsonResponse({
            'status': 'success',
            'item_total': float(item_total), # Ensure Decimal is JSON serializable
            'subtotal': float(subtotal),
            'total_price': float(total_price),
            'quantity': cart_item.quantity if not removed else 0,
            'removed': removed,
            'cart_item_count': total_quantity # Send total quantity
        })

    except Cart.DoesNotExist:
         return JsonResponse({'status': 'error', 'message': 'Item not found in cart.'}, status=404)
    except (ValueError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid quantity value.'}, status=400)
    except Exception as e:
         # Log the exception e
         return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred.'}, status=500)


# -----------------------------
# Clear Entire Cart
# -----------------------------
@login_required
def clear_cart(request):
    """ Removes all items from the user's cart. """
    # POST is safer for deletion actions
    # if request.method != 'POST':
    #    return HttpResponseBadRequest("POST method required.")

    Cart.objects.filter(user=request.user).delete()
    messages.success(request, "Cart cleared successfully.")
    return redirect('cart:cart_view')