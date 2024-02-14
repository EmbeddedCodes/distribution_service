from rest_framework.serializers import ModelSerializer

from payment.models import Payment


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
        depth = 1
