from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from drf_spectacular.utils import extend_schema


from payment.models import Payment, Order
from statistic.api.serializers import TotalOrdersSerializer, TotalOrdersByFlavorSerializer, \
    AvgOrderValueSerializer, FaildPaymentsSerializer, AvgProcessingTimeSerializer, \
    StatisticEndpointPerformanceSerializer, SuccessfulPaymentsSerializer
from statistic.models import EndpointPerformance


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: TotalOrdersSerializer},
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def total_orders(request):
    """
    Allows admin users, allowing them to retrieve the total number of orders placed within the system.
    """
    total_orders = Order.get_total_orders()

    serializer = TotalOrdersSerializer(data={"total_orders": total_orders})
    if serializer.is_valid():
        return Response(serializer.validated_data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: TotalOrdersByFlavorSerializer},
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def orders_by_flavor(request, flavor):
    """
    Allows admin users to retrieve the total number of orders for a specific ice cream flavor.
    """
    total_orders = Order.get_orders_by_flavor(flavor)
    serializer = TotalOrdersByFlavorSerializer(
        data={"total_orders": total_orders})
    if serializer.is_valid():
        return Response(serializer.validated_data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: AvgOrderValueSerializer},
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def average_order_value(request):
    """
    Computes and returns the average value of all orders.
    Admin user only.
    """
    avg_value = Order.get_average_order_value()
    serializer = AvgOrderValueSerializer(
        data={"average_order_value": avg_value})
    if serializer.is_valid():
        return Response(serializer.validated_data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: SuccessfulPaymentsSerializer},
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def successful_payments(request):
    """
    Retrieve the total count of successful payment transactions.
    Admin user only.
    """

    successful_payments = Payment.get_successful_payments()
    serializer = SuccessfulPaymentsSerializer(
        data={"successful_payments": successful_payments})
    if serializer.is_valid():
        return Response(serializer.validated_data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: FaildPaymentsSerializer},
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def failed_payments(request):
    """
    Retrieve the total count of faild payment transactions.
    Admin user only.
    """
    failed_payments = Payment.get_failed_payments()
    serializer = FaildPaymentsSerializer(
        data={"failed_payments": failed_payments})
    if serializer.is_valid():
        return Response(serializer.validated_data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: AvgProcessingTimeSerializer},
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def average_processing_time(request):
    """
     Provide the functionality to retrieve the average processing time of payment transactions.
     Admin use only.
    """
    avg_value = Payment.get_average_processing_time()
    serializer = AvgProcessingTimeSerializer(
        data={"average_processing_time": avg_value})
    if serializer.is_valid():
        return Response(serializer.validated_data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={
        status.HTTP_200_OK: StatisticEndpointPerformanceSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def endpoints_performance(request):
    """
    Providing a comprehensive overview of the performance metrics across various endpoints. 
    Admin user only.
    """
    data = EndpointPerformance.objects.all()
    serializer = StatisticEndpointPerformanceSerializer(data, many=True)

    return Response(serializer.data)
