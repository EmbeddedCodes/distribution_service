from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import IceCream
from .api.serializers import IceCreamSerializer
from django.contrib.auth.models import User


class IceCreamTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        IceCream.objects.create(
            title="Vanilla", flavor="vanilla", description="Classic vanilla", price=2.5)
        IceCream.objects.create(
            title="Chocolate", flavor="chocolate", description="Rich chocolate", price=3.0)

    def test_get_all_products(self):
        response = self.client.get(reverse('all_products'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)
        self.valid_payload = {
            "title": "New Flavor",
            "flavor": "Test Flavor",
            "description": "A new test flavor",
            "price": "4.99"
        }

    def test_create_product(self):
        response = self.client.post(
            reverse('create_product'), self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IceCream.objects.count(), 1)
        self.assertEqual(IceCream.objects.get().title, 'New Flavor')


class ProductDeleteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)
        self.ice_cream = IceCream.objects.create(
            title="Vanilla", flavor="vanilla", description="Classic", price=2.99)

    def test_delete_product(self):
        response = self.client.delete(reverse('delete_product', kwargs={
                                      'product_id': self.ice_cream.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(IceCream.objects.filter(
            id=self.ice_cream.id).exists())


class ProductUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)
        self.ice_cream = IceCream.objects.create(
            title="Original Flavor", flavor="original", description="Original", price=1.99)
        self.valid_payload = {
            "title": "Updated Flavor",
            "flavor": "updated",
            "description": "Updated description",
            "price": 2.99
        }

    def test_update_product_put(self):
        response = self.client.put(reverse('update_product', kwargs={
                                   'product_id': self.ice_cream.id}), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ice_cream.refresh_from_db()
        self.assertEqual(self.ice_cream.title, "Updated Flavor")

    def test_update_product_patch(self):
        patch_data = {"title": "Patched Flavor"}
        response = self.client.patch(reverse('update_product', kwargs={
                                     'product_id': self.ice_cream.id}), patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ice_cream.refresh_from_db()
        self.assertEqual(self.ice_cream.title, "Patched Flavor")
