from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import ValidationError

from core.models import Product
from shopping import serializers


class TesteadWriteSerializerMethodField(TestCase):
    pass  # TODO


class TestOrderDetailsSerializer(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.serializer_class = serializers.OrderDetailsSerializer
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
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.data.update({'status': 'CANCELED'})
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def test_validate_status_update_from_canceled(self):
        """When validating OrderDetailsSerializer
           and changing status from CANCELED
           validate_status method should raise ValidationError"""
        cancel_data = self.data.copy()
        cancel_data.update({'status': 'CANCELED'})

        serializer = self.serializer_class(data=cancel_data)
        serializer.is_valid(raise_exception=True)
        inst = serializer.save()

        serializer = self.serializer_class(data=self.data, instance=inst)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn(
            _('You cannot activate canceled order'),
            list(map(str, serializer.errors['status']))
        )


class TestCartItemSerializer(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.serializer_class = serializers.CartItemSerializer
        self.product = Product.objects.get(id=1)
        self.inventory = self.product.inventory

    def test_validate_valid_quantity(self):
        """When validating valid quantity nothing should happen"""
        data = {
            'product': self.product.id,
            'quantity': self.inventory.quantity - 1
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

    def test_validate_invalid_quantity(self):
        """When validating invalid quantity ValidationError will be raised"""
        data = {
            'product': self.product.id,
            'quantity': self.inventory.quantity + 1
        }
        serializer = self.serializer_class(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        self.assertIn(
            _(f"Product {self.product.id} quantity is bigger than its stock"),
            list(map(str, serializer.errors['non_field_errors']))
        )


class TestCartDetailsSerializer(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.serializer_class = serializers.CartDetailsSerializer
        p1 = Product.objects.get(id=1)
        p2 = Product.objects.get(id=1)
        self.data = {
            'items': [
                {
                    'product': p1.id,
                    'quantity': 2
                },
                {
                    'product': p2.id,
                    'quantity': 1
                }
            ],
            'total': 0
        }
        self.total = (p1.price * self.data['items'][0]['quantity'])\
            + (p2.price * self.data['items'][1]['quantity'])

    def test_create(self):
        """create method should create OrderDetails and OrderItems objects"""
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        self.assertAlmostEqual(
            self.data['items'][0]['product'],
            instance.items.all()[0].product.id
        )
        self.assertAlmostEqual(
            self.data['items'][1]['product'],
            instance.items.all()[1].product.id
        )

    def test_get_total_dict(self):
        """When given dict total will be calculated
          as a QuerySet Aggregation"""
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        self.assertEqual(serializer.data['total'], self.total)

    def test_get_total_ordered_dict(self):
        """When given OrderedDict total will be calculated
           based on given data input"""
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        self.assertEqual(instance.total, self.total)


class TestPaymentSerializer(TestCase):
    pass
