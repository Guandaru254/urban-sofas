# checkout/views.py (Updated checkout view)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# --- Ensure correct model imports ---
from orders.models import Order, OrderItem # Assuming Order models are in 'orders' app
from cart.models import Cart
from menu.models import MenuItem # Import MenuItem
# --- Ensure correct form import ---
from .forms import CheckoutForm # Assuming form is in checkout/forms.py
from decimal import Decimal
from django.urls import reverse # For namespaced redirects

# Define delivery fee (consider making this configurable later)
DELIVERY_FEE = Decimal('200.00')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('item') # Optimize
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add items before checking out.")
        # --- Use namespaced URL ---
        return redirect('cart:cart_view')

    # Calculate totals using Cart model method and delivery fee
    subtotal = sum(item.total_price() for item in cart_items if hasattr(item, 'total_price'))
    total_price = subtotal + DELIVERY_FEE

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Assuming payment method comes from the form or another POST field
            payment_method = form.cleaned_data.get('payment_method') # Or request.POST.get(...)
            # Extract phone number - ensure field name matches your CheckoutForm
            customer_phone_number = form.cleaned_data.get('phone_number') # Or 'mpesa_number' etc.

            # --- Create the Order instance ---
            try:
                order = Order.objects.create(
                    user=request.user,
                    # --- Save calculated totals and fee ---
                    subtotal=subtotal,
                    delivery_fee=DELIVERY_FEE,
                    total_price=total_price,
                    # --- Payment Info ---
                    payment_method=payment_method, # Ensure this matches choices in Order model
                    # payment_status='Pending', # Set initial payment status if field exists
                    # --- Customer Info (Snapshot) ---
                    customer_name=form.cleaned_data.get('customer_name', f"{request.user.first_name} {request.user.last_name}"), # Get from form or default
                    customer_phone=customer_phone_number,
                    # --- Delivery Info (from form) ---
                    delivery_address=form.cleaned_data['delivery_address'],
                    delivery_city=form.cleaned_data.get('delivery_city', ''), # Use .get for optional fields
                    delivery_postal_code=form.cleaned_data.get('delivery_postal_code', ''),
                    special_instructions=form.cleaned_data.get('special_instructions', ''),
                    # --- Order Status ---
                    status='Pending' # Initial status
                )

                # --- Create OrderItem instances ---
                order_items_to_create = []
                for cart_item in cart_items:
                    order_items_to_create.append(
                        OrderItem(
                            order=order,
                            # --- Use correct field name and link to MenuItem ---
                            menu_item=cart_item.item,
                            # --- SAVE PRICE AT TIME OF ORDER ---
                            price_per_unit=cart_item.item.price,
                            quantity=cart_item.quantity
                        )
                    )
                # Create all items efficiently
                OrderItem.objects.bulk_create(order_items_to_create)

                # --- Clear the user's cart ---
                cart_items.delete()

                messages.success(request, "Order placed successfully! Awaiting payment confirmation.") # Updated message

                # TODO: Initiate Payment Process Here (e.g., M-Pesa STK Push)
                # if payment_method == 'mpesa':
                #    initiate_stk_push(order=order, phone_number=customer_phone_number, amount=total_price)
                #    return redirect('payments:payment_pending', order_id=order.id) # Redirect to a pending page

                # --- Redirect to success page (use namespaced URL) ---
                # This might happen AFTER payment confirmation in a real scenario
                return redirect('checkout:order_success', order_id=order.id)

            except Exception as e:
                # Log the error e
                messages.error(request, "An error occurred while creating your order. Please try again.")
                # Optionally: redirect back to cart or show specific error page

        else: # Form is invalid
            messages.error(request, "There was an error with your checkout details. Please check the form below.")
            # Fall through to render the form again with errors

    else: # GET request
        # Pre-populate form with profile data if available?
        # initial_data = {}
        # if hasattr(request.user, 'profile'):
        #    initial_data['customer_name'] = f"{request.user.first_name} {request.user.last_name}"
        #    initial_data['phone_number'] = request.user.profile.phone_number
        #    initial_data['delivery_address'] = request.user.profile.address
        #    initial_data['delivery_city'] = request.user.profile.city
        #    initial_data['delivery_postal_code'] = request.user.profile.postal_code
        # form = CheckoutForm(initial=initial_data)
        form = CheckoutForm() # Basic empty form


    # Render checkout page for GET request or if POST form was invalid
    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': DELIVERY_FEE,
        'total_price': total_price
    }
    return render(request, 'checkout/checkout.html', context)


@login_required
def order_success(request, order_id):
    """ Displays the order confirmation page. """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'checkout/order_success.html', context)

# Placeholder - purpose needs defining in the checkout flow
# def payment(request):
#     """ Handles specific payment steps or confirmation? """
#     return render(request, 'checkout/payment.html')