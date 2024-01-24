from rest_framework import serializers

from .models import Discount, Product, ProductCategory, ProductInventory


class ProductSerializer(serializers.ModelSerializer):
    serializer_class = Product
    queryset = Product.objects.all()

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1


class ProductInventorySerializer(serializers.ModelSerializer):
    serializer_class = ProductInventory
    queryset = ProductInventory.objects.all()

    class Meta:
        model = ProductInventory
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    serializer_class = ProductCategory
    queryset = ProductCategory.objects.all()

    class Meta:
        model = ProductCategory
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    serializer_class = Discount
    queryset = Discount.objects.all()

    class Meta:
        model = Discount
        fields = '__all__'
