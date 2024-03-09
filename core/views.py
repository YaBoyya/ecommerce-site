from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from core import serializers
from core.mixins import ProductSearchMixin, SearchMixin
from core.models import Discount, Product, ProductCategory, ProductInventory


class IndexViewSet(ProductSearchMixin,
                   viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = serializers.ProductSerializer


class ProductManagementViewSet(ProductSearchMixin,
                               viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAdminUser]


class ProductCategoryManagement(SearchMixin,
                                viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer
    permission_classes = [IsAdminUser]


class ProductInventoryManagement(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = serializers.ProductInventorySerializer
    permission_classes = [IsAdminUser]


class DiscountManagement(SearchMixin,
                         viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = serializers.DiscountSerializer
    permission_classes = [IsAdminUser]
