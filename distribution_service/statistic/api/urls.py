
from statistic.api.views import orders_by_flavor, average_processing_time, endpoints_performance, \
    total_orders, average_order_value, successful_payments, failed_payments
from django.urls import path


urlpatterns = [
    path('total-orders/', total_orders, name='total_orders'),
    path('orders-by-flavor/<str:flavor>/',
         orders_by_flavor, name='orders_by_flavor'),
    path('average-oder-value/', average_order_value, name='average_order_value'),
    path('successful-payments/', successful_payments, name='successful_payments'),
    path('faild-payments/', failed_payments, name='failed_payments'),
    path('average-processing-time/', average_processing_time,
         name='average_processing_time'),
    path('endpoints-performance/', endpoints_performance,
         name='endpoints_performance'),

]
