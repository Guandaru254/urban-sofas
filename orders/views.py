from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from .forms import OrderForm
from menu.models import MenuItem

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save the basic order details
            order = form.save(commit=False)
            order.user = request.user  # Assuming user is logged in
            order.total_price = 0  # This will be calculated later
            order.save()

            # Add selected menu items (this part requires a front-end solution)
            menu_item_ids = request.POST.getlist('menu_items')  # Assuming menu_items are passed as a POST parameter
            for item_id in menu_item_ids:
                menu_item = MenuItem.objects.get(id=item_id)
                quantity = int(request.POST.get(f'quantity_{item_id}', 1))
                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)
                order.total_price += menu_item.price * quantity

            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()
        menu_items = MenuItem.objects.all()  # Display all menu items for selection
    return render(request, 'orders/create_order.html', {'form': form, 'menu_items': menu_items})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})