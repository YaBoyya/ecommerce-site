from rest_framework import viewsets

from core import serializers
from core.mixins import ProductSearchMixin, SearchMixin
from core.models import Discount, Product, ProductCategory, ProductInventory
from core.permissions import IsStaff


class IndexViewSet(ProductSearchMixin,
                   viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = serializers.ProductSerializer


class ProductManagementViewSet(ProductSearchMixin,
                               viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsStaff]


class ProductCategoryManagement(SearchMixin,
                                viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer
    permission_classes = [IsStaff]


class ProductInventoryManagement(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = serializers.ProductInventorySerializer
    permission_classes = [IsStaff]


class DiscountManagement(SearchMixin,
                         viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = serializers.DiscountSerializer
    permission_classes = [IsStaff]
