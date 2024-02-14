
from django.urls import path

from order.api.views import add_item_to_cart, delete_item_from_cart, get_cart_details, empty_cart, create_order

urlpatterns = [
    path('add-item-to-cart/<int:product_id>/',
         add_item_to_cart, name='add_item_to_cart'),
    path('delete-from-cart/<int:item_id>/',
         delete_item_from_cart, name='delete_item_from_cart'),
    path('cart-details/',
         get_cart_details, name='get_cart_details'),
    path('empty-cart/<int:cart_id>/',
         empty_cart, name='empty_cart'),
    path('create-order/<int:cart_id>/', create_order, name='create_order'),
]
