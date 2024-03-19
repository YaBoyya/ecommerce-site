from django.urls import reverse

from rest_framework.test import APITestCase

from knox.models import AuthToken

from core.models import Product, ProductCategory, ProductInventory
from users.models import ECommerceUser


class TestSearchMixin(APITestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.url = reverse('core:m-product-category-list')
        self.user = ECommerceUser.objects.create_superuser(
            username='admin',
            email='admin@email.com',
            password='Admin123'
        )
        self.token = f'Token {AuthToken.objects.create(user=self.user)[-1]}'

    def test_list_search(self):
        """Listing view will return correct items"""
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['count'], 10)

        response = self.client.get(
            self.url,
            {'q': 'test1'},
            format='json'
        )
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(
            self.url,
            {'q': 'incorrect'},
            format='json'
        )
        self.assertEqual(response.data['count'], 0)


class TestProductSearchMixin(APITestCase):
    def setUp(self):
        self.url = reverse('core:index-list')
        self.category = ProductCategory.objects.create(
            name='category',
            desc='desc1'
        )
        self.inventory1 = ProductInventory.objects.create(quantity=10)
        self.inventory2 = ProductInventory.objects.create(quantity=5)
        self.product1 = Product.objects.create(
            name='test1',
            desc='desc1',
            SKU='sku1',
            price='1.1',
            category=self.category,
            inventory=self.inventory1)
        self.product2 = Product.objects.create(
            name='test2',
            desc='desc2',
            SKU='sku2',
            price='1.1',
            category=self.category,
            inventory=self.inventory2)

    def test_list_search(self):
        """Listing view will return correct products"""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(
            reverse('core:index-list'),
            {'q': self.product1.name},
            format='json'
        )
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(
            self.url,
            {'q': self.category.name},
            format='json'
        )
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(
            self.url,
            {'q': 'incorrect'},
            format='json'
        )
        self.assertEqual(response.data['count'], 0)
