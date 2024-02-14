from django.test import TestCase
from unittest import mock
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User


class TotalOrdersTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)

    @mock.patch('order.models.Order.get_total_orders')
    def test_total_orders(self, mock_get_total_orders):
        # Mock the total orders count
        mock_get_total_orders.return_value = 5
        url = reverse('total_orders')

        response = self.client.get(url)

        # Assert the status code and orders count
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_orders'], 5)


class OrdersByFlavorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)

    @mock.patch('order.models.Order.get_orders_by_flavor')
    def test_orders_by_flavor(self, mock_get_orders_by_flavor):
        # Mock the return value of get_orders_by_flavor
        mock_get_orders_by_flavor.return_value = 5
        url = reverse('orders_by_flavor', kwargs={'flavor': 'vanilla'})

        response = self.client.get(url)

        # Assert the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_orders'], 5)


class AverageOrderValueTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)

    @mock.patch('order.models.Order.get_average_order_value')
    def test_average_order_value(self, mock_avg_order_value):
        # Mock the average order value
        mock_avg_order_value.return_value = 100.00

        url = reverse('average_order_value')

        response = self.client.get(url)

        # Assert the status code and average order value
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_order_value'], 100.00)


class SuccessfulPaymentsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)

    @mock.patch('payment.models.Payment.get_successful_payments')
    def test_successful_payments(self, mock_successful_payments):
        # Mock the successful payments count
        mock_successful_payments.return_value = 150

        url = reverse('successful_payments')

        response = self.client.get(url)

        # Assert the status code and successful payments count
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['successful_payments'], 150)


class FailedPaymentsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)

    @mock.patch('payment.models.Payment.get_failed_payments')
    def test_failed_payments(self, mock_failed_payments):
        # Mock the failed payments count
        mock_failed_payments.return_value = 50

        url = reverse('failed_payments')

        response = self.client.get(url)

        # Assert the status code and failed payments count
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['failed_payments'], 50)


class AverageProcessingTimeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)

    @mock.patch('payment.models.Payment.get_average_processing_time')
    def test_average_processing_time(self, mock_avg_processing_time):
        # Mock the average processing time value
        mock_avg_processing_time.return_value = 120

        url = reverse('average_processing_time')

        response = self.client.get(url)

        # Assert the status code and the average processing time
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_processing_time'], 120)
