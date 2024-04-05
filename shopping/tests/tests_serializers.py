from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import ValidationError

from core.models import Product
from shopping.serializers import CartItemSerializer, OrderDetailsSerializer


class TestOrderDetailsSerializer(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.data = {
            'user': 1,
            'status': 'OPEN',
            'total': 12,
            'items': [
                {
                    'product': 1,
                    'quantity': 2
                }
            ]
        }

    def test_validate_status_valid(self):
        """When validating OrderDetailsSerializer with valid data,
           validate_status method shouldn't raise anything"""
        serializer = OrderDetailsSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.data.update({'status': 'CANCELED'})
        serializer = OrderDetailsSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def test_validate_status_update_from_canceled(self):
        """When validating OrderDetailsSerializer
           and changing status from CANCELED
           validate_status method should raise ValidationError"""
        cancel_data = self.data.copy()
        cancel_data.update({'status': 'CANCELED'})

        serializer = OrderDetailsSerializer(data=cancel_data)
        serializer.is_valid(raise_exception=True)
        inst = serializer.save()

        serializer = OrderDetailsSerializer(data=self.data, instance=inst)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn(
            _('You cannot activate canceled order'),
            list(map(str, serializer.errors['status']))
        )


class TestCartItemSerializer(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.product = Product.objects.get(id=1)
        self.inventory = self.product.inventory

    def test_validate_valid_quantity(self):
        """When validating valid quantity nothing should happen"""
        data = {
            'product': self.product.id,
            'quantity': self.inventory.quantity - 1
        }
        serializer = CartItemSerializer(data=data)
        serializer.is_valid(raise_exception=True)

    def test_validate_invalid_quantity(self):
        """When validating invalid quantity ValidationError will be raised"""
        data = {
            'product': self.product.id,
            'quantity': self.inventory.quantity + 1
        }
        serializer = CartItemSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        self.assertIn(
            _(f"Product {self.product.id} quantity is bigger than its stock"),
            list(map(str, serializer.errors['non_field_errors']))
        )
