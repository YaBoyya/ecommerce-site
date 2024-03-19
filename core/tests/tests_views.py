from django.urls import reverse

from rest_framework.test import APIRequestFactory, APITestCase

from core import serializers
from core.models import Product


class TestIndexViewSet(APITestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.factory = APIRequestFactory()
        self.product = Product.objects.first()

    def test_details_view_serializer(self):
        """Details view uses expected serializer"""
        serializer = serializers.ProductSerializer(self.product)
        response = self.client.get(
            reverse('core:index-detail',
                    kwargs={'pk': self.product.id, 'format': 'json'}))
        self.assertEqual(response.data, serializer.data)

    def test_list_view_serializer(self):
        """List view uses expected serializer"""
        serializer = serializers.FeedSerializer(self.product)
        response = self.client.get(
            reverse('core:index-list',
                    kwargs={'format': 'json'}))
        self.assertEqual(response.data['results'][0], serializer.data)
