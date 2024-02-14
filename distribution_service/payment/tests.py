from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status

from order.models import Order
from payment.models import Payment


class GetAllPaymentsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.user = User.objects.create_user(
            username='user', password='password')
        self.order = Order.objects.create(
            order_number=1234, created_by=self.user)
        Payment.objects.create(order=self.order, amount=9.99)
        self.url = reverse('all_payments')

    def test_get_payments_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming there are payments in the database
        self.assertTrue(len(response.data) > 0)

    def test_get_payments_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the user can only see their payments
        for payment in response.data:
            self.assertEqual(payment['order']['created_by'], self.user.id)


class GetPaymentDetailsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user', password='password')
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.order = Order.objects.create(
            order_number=12345, created_by=self.user)
        self.payment = Payment.objects.create(
            order=self.order, amount=100.00, payment_id='P123')
        self.url = reverse('get_payment', kwargs={
                           'payment_id': self.payment.payment_id})

    def test_get_payment_as_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payment_id'], self.payment.payment_id)

    def test_get_payment_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payment_id'], self.payment.payment_id)
