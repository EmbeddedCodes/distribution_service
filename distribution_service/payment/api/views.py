from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

import django_rq
import random
import time
import logging

from payment.api.serializers import PaymentSerializer
from payment.models import Payment

logger = logging.getLogger(__name__)


def update_order_and_payment(order, payment, payment_status, start_time):
    payment.payment_status = payment_status
    payment.processing_time_seconds = time.time() - start_time
    payment.save()

    if payment_status == 'successful':
        order.status = 'paid'
        order.save()


def process_payment(order, payment):
    """
        This function simulate a payment process adding a delay and randomly generating an output.
        Output can be either False or True.
        It takes (order, payment) as parameters and calls "update_order_and_payment" to update
        both order and payment data.
    """
    logger.info(f'payment for order {order.order_number} initiated')
    start_time = time.time()
    time.sleep(random.randint(1, 10))  # Simulate processing delay
    payment_successful = random.choice([True, False])
    if payment_successful:
        update_order_and_payment(order, payment, 'successful', start_time)
        logger.info(f'payment for order {order.order_number} successful')
    else:
        logger.error(f"Payment for order {order.order_number} failed.")
        update_order_and_payment(order, payment, 'faild', start_time)
    return payment_successful


def create_and_process_payment(order):
    """
        Create an initiate the payment.
        Returns payment details
    """
    print(order)
    payment = Payment.objects.create(
        order=order, amount=order.total, payment_id=f"PAY{order.order_number}")
    payment.save()

    queue = django_rq.get_queue('default')
    queue.enqueue(process_payment, order, payment)

    serializer = PaymentSerializer(payment)

    return Response(serializer.data)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: PaymentSerializer},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_payments(request):
    """
    Retrieve list of transactions
    Superusers can view all payments across the platform, 
    while other authenticated users can only see payments related to their own orders. 
    The response provid detailed information on each payment in a structured format.
    """
    if request.user.is_superuser:
        payments = Payment.objects.all()
    else:
        payments = Payment.objects.filter(order__created_by=request.user)

    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@extend_schema(
    request=PaymentSerializer,
    responses={status.HTTP_200_OK: PaymentSerializer},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment(request, payment_id):
    """
    Allows authenticated usersto retrieve details of a specific payment transaction identified by payment_id. 
    Superusers have the privilege to access any payment's details, whereas other users can only fetch details of payments associated with their own orders.
    """
    if request.user.is_superuser:
        payment = get_object_or_404(Payment, payment_id=payment_id)
    else:
        payment = get_object_or_404(
            Payment, payment_id=payment_id, order__created_by=request.user)

    serializer = PaymentSerializer(payment)
    return Response(serializer.data)
