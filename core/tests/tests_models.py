from django.test import TestCase

from core.models import Product, ProductCategory, ProductInventory


class TestECommerceModel(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(
            name='test', desc='test')
        self.inventory = ProductInventory.objects.create(quantity=10)
        self.product_data = {
            'name': 'test',
            'desc': "It's a test",
            'SKU': 'SKUNUMBER',
            'price': '12.73',
            'category': self.category,
            'inventory': self.inventory
        }
        self.model = Product.objects.create(**self.product_data)

    def test_save(self):
        """
        After saving modified_at field will be updated
        """
        self.assertIsNone(self.model.modified_at)
        self.model.save()
        self.assertIsNotNone(self.model.modified_at)

    def test_delete(self):
        """
        After deleting deleted_at field will be updated and modified_at won't
        """
        modified_at = self.model.modified_at
        self.assertIsNone(self.model.deleted_at)
        self.model.delete()
        self.assertIsNotNone(self.model.deleted_at)
        self.assertEqual(self.model.modified_at, modified_at)
