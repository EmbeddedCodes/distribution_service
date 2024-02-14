
from django.urls import path

from order.views import add_to_cart, cart_details, delete_from_cart, submit_order

urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('delete-from-cart/<int:item_id>/',
         delete_from_cart, name='delete_from_cart'),
    path('cart-details/', cart_details, name='cart_details'),
    path('submit-order/<int:cart_id>/', submit_order, name='submit_order'),
]
