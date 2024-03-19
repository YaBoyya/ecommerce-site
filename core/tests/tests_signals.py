from django.test import TestCase

from core.models import Product, ProductInventory


class TestDeleteProductInvetory(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.product = Product.objects.get(id=1)

    def test_signal_works_correctly(self):
        """After deleting Product,
           delete method will be called on ProductInventory"""
        self.product.delete()

        self.assertIsNotNone(self.product.inventory.deleted_at)


class TestDeleteProduct(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.inventory = ProductInventory.objects.get(id=1)

    def test_signal_works_correctly(self):
        """After deleting ProductInventory,
           delete method will be called on Product"""
        self.inventory.delete()

        self.assertIsNotNone(self.inventory.product.deleted_at)
