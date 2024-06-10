from django.db.models import Q
from django.test import TestCase

from core.models import Product
from core.serializers import FeedSerializer, ProductSerializer


class TestFeedSerializer(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.product = Product.objects.filter(
            ~Q(discount=None)
            & Q(discount__is_active=True)
        ).first()
        self.product_no_disc = Product.objects.filter(
            Q(discount=None)
            | Q(discount__is_active=False)
        ).first()
        self.serializer = ProductSerializer(self.product)
        self.serializer_no_disc = ProductSerializer(self.product_no_disc)

    def test_contains_expected_fields(self):
        """Feed serializer consists of expected fields"""
        data = self.serializer.data
        self.assertEqual(list(data.keys()), FeedSerializer.Meta.fields)


class TestProductSerializer(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.product = Product.objects.filter(
            ~Q(discount=None)
            & Q(discount__is_active=True)
        ).first()
        self.product_no_disc = Product.objects.filter(
            Q(discount=None)
            | Q(discount__is_active=False)
        ).first()
        self.serializer = ProductSerializer(self.product)
        self.serializer_no_disc = ProductSerializer(self.product_no_disc)

    def test_category_field_content(self):
        """Category field has expected content"""
        data = {
            'id': self.product.category.id,
            'name': self.product.category.name,
            'desc': self.product.category.desc
        }
        self.assertEqual(self.serializer.data['category'], data)

    def test_discount_field_content_not_exists(self):
        """Discount field returns none if product has no associated discount"""
        self.assertEqual(self.serializer_no_disc.data['discount'], None)

    def test_discount_field_content_exists(self):
        """Discount field has expected content"""
        data = {
            'id': self.product.discount.id,
            "name": self.product.discount.name,
            "desc": self.product.discount.desc,
            "discount_percent": self.product.discount.discount_percent,
            "discounted_price":
                round(
                    self.product.price * (
                        100 - self.product.discount.discount_percent) / 100,
                    2
                )
        }
        self.assertEqual(self.serializer.data['discount'], data)
