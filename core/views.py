from rest_framework import viewsets

from . import serializers
from .mixins import ProductSearchMixin, SearchMixin
from .models import Discount, Product, ProductCategory, ProductInventory


class IndexViewSet(ProductSearchMixin,
                   viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = serializers.ProductSerializer


# TODO restrict to only staff members
class ProductManagementViewSet(ProductSearchMixin,
                               viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductCategoryManagement(SearchMixin,
                                viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer


class ProductInventoryManagement(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = serializers.ProductInventorySerializer


class DiscountManagement(SearchMixin,
                         viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = serializers.DiscountSerializer
