from rest_framework import serializers

from .models import Discount, Product, ProductCategory, ProductInventory


class ProductSerializer(serializers.ModelSerializer):
    serializer_class = Product
    queryset = Product.objects.all()

    category = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_category(self, obj):
        return {"id": obj.category.id,
                "name": obj.category.name,
                "desc": obj.category.desc}

    def get_discount(self, obj):
        return {
            "id": obj.discount.id,
            "discount_percent": obj.discount.discount_percent,
            "discounted_price": round(
                obj.price * (100 - obj.discount.discount_percent) / 100,
                2)
            } if obj.discount and obj.discount.is_active else None

    def get_inventory(self, obj):
        return {"id": obj.inventory.id,
                "quantity": obj.inventory.quantity}


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
