from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import ValidationError

from shopping.serializers import OrderDetailsSerializer


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

        # print(self.data, cancel_data)

        serializer = OrderDetailsSerializer(data=cancel_data)
        serializer.is_valid(raise_exception=True)
        inst = serializer.save()
        # print(inst.status, self.data['status'])

        serializer = OrderDetailsSerializer(data=self.data, instance=inst)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        # serializer.save()
        self.assertIn(
            _('You cannot activate canceled order'),
            list(map(str, serializer.errors['status']))
        )
        print(serializer.errors)
