from rest_framework.serializers import ModelSerializer, Serializer, IntegerField, DecimalField, FloatField

from statistic.models import EndpointPerformance


class TotalOrdersSerializer(Serializer):
    total_orders = IntegerField(help_text="Total number of orders")


class TotalOrdersByFlavorSerializer(Serializer):
    total_orders = IntegerField(help_text="Total number of orders by flavor")


class AvgOrderValueSerializer(Serializer):
    average_order_value = DecimalField(
        max_digits=12, decimal_places=2, help_text="Average order value")


class SuccessfulPaymentsSerializer(Serializer):
    successful_payments = IntegerField(help_text="Total successful payment")


class FaildPaymentsSerializer(Serializer):
    failed_payments = IntegerField(help_text="Total failed payment")


class AvgProcessingTimeSerializer(Serializer):
    average_processing_time = FloatField(help_text="Total faild payment")


class StatisticEndpointPerformanceSerializer(ModelSerializer):

    class Meta:
        model = EndpointPerformance
        fields = "__all__"
