from django.urls import reverse

from rest_framework.test import APITestCase

from core.models import Product, ProductCategory, ProductInventory


class TestSearchMixin(APITestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(
            name='test', desc='test')
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
            price='2.2',
            category=self.category,
            inventory=self.inventory2)

    def test_list_search(self):
        response = self.client.get(reverse('core:index-list'), format='json')
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(reverse('core:index-list'),
                                   {'q': self.product1.name},
                                   format='json')
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(reverse('core:index-list'),
                                   {'q': 'incorrect'},
                                   format='json')
        self.assertEqual(response.data['count'], 0)


class TestProductSearchMixin(APITestCase):
    def setUp(self):
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
        response = self.client.get(reverse('core:index-list'), format='json')
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(reverse('core:index-list'),
                                   {'q': self.product1.name},
                                   format='json')
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(reverse('core:index-list'),
                                   {'q': self.category.name},
                                   format='json')
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(reverse('core:index-list'),
                                   {'q': 'incorrect'},
                                   format='json')
        self.assertEqual(response.data['count'], 0)
