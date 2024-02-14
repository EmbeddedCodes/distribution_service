from django.urls import path

from payment.api.views import process_payment, get_all_payments, get_payment

urlpatterns = [
    path('process-payment/', process_payment, name='process-payment'),
    path('all-payments/', get_all_payments, name='all_payments'),
    path('payment/<str:payment_id>/', get_payment, name='get_payment')
]
