from rest_framework.serializers import ModelSerializer

from ice_cream.models import IceCreamItem, IceCream


class IceCreamRequestSerializer(ModelSerializer):
    class Meta:
        model = IceCream
        fields = ['title', 'flavor', 'description', 'price']


class IceCreamSerializer(ModelSerializer):

    class Meta:
        model = IceCream
        fields = "__all__"


class IceCreamItemSerializer(ModelSerializer):

    ice_cream = IceCreamSerializer()

    class Meta:
        model = IceCreamItem
        fields = ['id', 'quantity', 'ice_cream', 'created_at']
