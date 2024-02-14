from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from django.db.models import Max, F, Sum
import logging

from ice_cream.models import IceCream, IceCreamItem
from order.api.serializers import OrderSerializer, CartSerializer
from order.models import Cart, Order
from payment.api.views import create_and_process_payment

logger = logging.getLogger(__name__)


@extend_schema(
    request=None,
    responses={status.HTTP_201_CREATED: OrderSerializer},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request, cart_id=None):
    """
        Submit an order. Items from the cart will be added to the order.
        The total cost is calculated for payment, which is then queued for processing. 
        This function returns the order details. A valid cart_id must be provided.
    """
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
    logger.info(f"Order {order.order_number} has been created")

    cart.items.clear()
    logger.info(f"Cart with ID :  {cart_id} has been cleared")
    print(order)
    create_and_process_payment(order)

    serializer = OrderSerializer(order)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: CartSerializer},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item_to_cart(request, product_id=None):
    """
        Create an item for the product identified by product_id. It ensures a cart exists for the user, 
        either by retrieving an existing one or creating a new one, 
        before proceeding to add the specified item.
        product_id is required
    """
    user = request.user
    # validate and get ice-cream product
    ice_cream = get_object_or_404(IceCream, id=product_id)
    quantity = request.data.get('quantity', 1)

    cart, _ = Cart.objects.get_or_create(user=user)

    # create shopping item
    item = IceCreamItem.objects.create(
        ice_cream=ice_cream, quantity=quantity)

    cart.items.add(item)
    cart.save()
    logger.info(f"Item  for product {product_id} added to cart")
    serializer = CartSerializer(cart)

    return Response(serializer.data)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: CartSerializer},
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item_from_cart(request, item_id=None):
    """
    Allows authenticated users to remove a specific item, identified by item_id, 
    from their shopping cart
    item_id is required
    """
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(IceCreamItem, id=item_id, cart=cart)
    cart.items.remove(item)
    logger.info(f"Item with ID {item_id} removed from cart")
    serializer = CartSerializer(cart)

    return Response(serializer.data)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: CartSerializer},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_details(request):
    """
    Enables authenticated users to retrieve the details of their current shopping cart, if existed.
    """
    cart = get_object_or_404(Cart, user=request.user)

    serializer = CartSerializer(cart)

    return Response(serializer.data)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: CartSerializer},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empty_cart(request, cart_id=None):
    """
    Allows authenticated user to remove all items from their cart.
    Allows admin user to empty cart givven it's id.
    """
    if request.user.is_superuser:
        cart = get_object_or_404(Cart, id=cart_id)
    else:
        cart = get_object_or_404(Cart, user=request.user)

    cart.items.clear()
    logger.info(
        f"Cart with ID {cart_id} was emptied by {request.user.username}")
    serializer = CartSerializer(cart)

    return Response(serializer.data)
