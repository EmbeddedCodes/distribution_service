from django.urls import path

from ice_cream.api.views import get_all_products, create_product, delete_product, update_product

urlpatterns = [
    path('all-products/', get_all_products, name='all_products'),
    path('create-product/', create_product, name='create_product'),
    path('delete-product/<int:product_id>/',
         delete_product, name='delete_product'),
    path('update-product/<int:product_id>/',
         update_product, name='update_product'),
]
