from django.urls import reverse

from rest_framework.test import APITestCase

from core.models import Product, ProductCategory


class TestSearchMixin(APITestCase):
    def setUp(self):
        self.product1 = Product.objects.create(
            name='test1',
            desc='desc1',
            SKU='sku1',
            price='1.1')
        self.product2 = Product.objects.create(
            name='test2',
            desc='desc2',
            SKU='sku2',
            price='2.2')

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
        self.product1 = Product.objects.create(
            name='test1',
            desc='desc1',
            SKU='sku1',
            category_id=self.category,
            price='1.1')
        self.product2 = Product.objects.create(
            name='test2',
            desc='desc2',
            SKU='sku2',
            category_id=self.category,
            price='2.2')

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
