from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import IceCream, Cart, IceCreamItem, Order
from django.contrib.auth.models import User


class AddItemToCartTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user', password='password')
        self.client.force_authenticate(user=self.user)
        self.ice_cream = IceCream.objects.create(
            title="Chocolate", flavor="chocolate", price=2.50)
        self.url = reverse('add_item_to_cart', kwargs={
                           'product_id': self.ice_cream.id})

    def test_add_item_to_cart(self):
        response = self.client.post(self.url, {'quantity': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        item = cart.items.first()
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.ice_cream.id, self.ice_cream.id)


class DeleteItemFromCartTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user', password='password')
        self.client.force_authenticate(self.user)
        self.ice_cream = IceCream.objects.create(
            title="Strawberry", flavor="strawberry", price=3.00)
        self.cart = Cart.objects.create(user=self.user)
        self.item = IceCreamItem.objects.create(
            ice_cream=self.ice_cream, quantity=1)
        self.cart.items.add(self.item)
        self.url = reverse('delete_item_from_cart', kwargs={
                           'item_id': self.item.id})

    def test_delete_item_from_cart(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertFalse(self.cart.items.filter(id=self.item.id).exists())


class GetCartDetailsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user', password='password')
        self.client.force_authenticate(user=self.user)
        self.cart = Cart.objects.create(user=self.user)
        self.url = reverse('get_cart_details')

    def test_get_cart_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check for key response fields in the cart serializer
        self.assertIn('id', response.data)
        self.assertIn('items', response.data)
        self.assertEqual(response.data['id'], self.cart.id)


class EmptyCartTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user', password='password')
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.cart = Cart.objects.create(user=self.user)
        self.ice_cream = IceCream.objects.create(
            title="Mint", flavor="mint", price=2.99)
        self.item = IceCreamItem.objects.create(
            ice_cream=self.ice_cream, quantity=2)
        self.cart.items.add(self.item)
        self.url = reverse('empty_cart', kwargs={'cart_id': self.cart.id})

    def test_empty_cart_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.count(), 0)

    def test_empty_cart_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.count(), 0)


class CreateOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user', password='password')
        self.client.force_authenticate(user=self.user)
        self.ice_cream = IceCream.objects.create(
            title="Vanilla", flavor="vanilla", price=2.5)
        self.ice_cream_item = IceCreamItem.objects.create(
            ice_cream=self.ice_cream, quantity=2)
        self.cart = Cart.objects.create(user=self.user)
        self.cart.items.add(self.ice_cream_item)
        self.url = reverse('create_order', kwargs={'cart_id': self.cart.id})

    def test_create_order(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.exists())
        order = Order.objects.first()
        self.assertEqual(order.created_by, self.user)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first(), self.ice_cream)
