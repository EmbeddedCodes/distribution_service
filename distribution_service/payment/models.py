from django.db import models

from helper.model import Meta
from order.models import Order


class Payment(Meta):
    """
    The Payment model extends Meta to manage payment information related to orders. 
    It uniquely associates each payment with an order, tracking payment ID, status, 
    amount, and processing time in seconds. This model ensures each payment is linked 
    to a specific order and provides methods to count successful and failed payments,
    as well as calculate the average processing time, aiding in the analysis and 
    reporting of payment transactions within the system.
    """
    order = models.OneToOneField(
        Order, related_name='payment', on_delete=models.CASCADE,
        help_text="The associated order for this payment.")
    payment_id = models.CharField(max_length=200, default='PAY1111',
                                  help_text="Unique identifier for the payment transaction.")
    payment_status = models.CharField(max_length=200, default='PENDING',
                                      help_text="Current status of the payment (e.g., PENDING, SUCCESSFUL, FAILED).")
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, help_text="Total amount of the payment.")
    processing_time_seconds = models.FloatField(default=5,
                                                help_text="The duration in seconds that the payment processing took.")

    class Meta(Meta.Meta):
        unique_together = [("order", "payment_id")]

    def __str__(self) -> str:
        return f'payment for {self.order.order_number} at {self.created_at}'

    @classmethod
    def get_successful_payments(cls):
        return cls.objects.filter(payment_status='successful').count()

    @classmethod
    def get_failed_payments(cls):
        return cls.objects.filter(payment_status='faild').count()

    @classmethod
    def get_average_processing_time(cls):
        return cls.objects.annotate(avg_value=models.F('processing_time_seconds')).aggregate(models.Avg('avg_value'))
