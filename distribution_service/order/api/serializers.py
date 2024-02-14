from rest_framework.serializers import ModelSerializer

from ice_cream.api.serializers import IceCreamItemSerializer
from order.models import Order, Cart


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class CartSerializer(ModelSerializer):
    items = IceCreamItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']
