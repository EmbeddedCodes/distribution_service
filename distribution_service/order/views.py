from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import F, Sum, Max
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
from ice_cream.models import IceCreamItem, IceCream
from order.models import Cart, Order
from payment.api.views import create_and_process_payment

logger = logging.getLogger(__name__)


@login_required
def cart_details(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.prefetch_related('ice_cream')
        cart_id = cart.id
    except Cart.DoesNotExist:
        items = None
        cart_id = None
    return render(request, 'checkout/cart_details.html', {'cart_items': items, 'cart_id': cart_id})


@login_required
def add_to_cart(request, product_id=None):
    quantity = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError("Invalid quantity")
    except ValueError:
        messages.error(request, "Invalid quantity.")
        return redirect('ice_cream_list')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    ice_cream = get_object_or_404(IceCream, id=product_id)

    item = IceCreamItem.objects.create(
        ice_cream=ice_cream, quantity=quantity)

    cart.items.add(item)

    messages.success(request, "Item added to cart successfully.")
    return redirect('ice_cream_list')


@login_required
def delete_from_cart(request, item_id=None):
    # Ensures cart exists for the user
    cart = get_object_or_404(Cart, user=request.user)
    # Validates item is in user's cart
    item = get_object_or_404(IceCreamItem, id=item_id, cart=cart)
    cart.items.remove(item)

    return redirect('cart_details')


@login_required
def submit_order(request, cart_id=None):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    items = cart.items.prefetch_related('ice_cream')

    last_order_number = Order.objects.all().aggregate(
        Max('order_number'))['order_number__max']

    next_order_number = (last_order_number or 1000) + 1
    order = Order.objects.create(
        order_number=next_order_number, created_by=request.user)

    total = items.annotate(item_total=Sum(
        F('quantity') * F('ice_cream__price'))).aggregate(total=Sum('item_total'))['total']
    order.items.add(*[item.ice_cream for item in items])
    order.total = total or 0
    order.save()
    cart.items.clear()
    create_and_process_payment(order)

    return render(request, 'checkout/order_submited.html', {'order_number': order.order_number})
