from rest_framework import serializers

from core import models


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
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

    def get_rating(self, obj):
        return obj.rating


class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductInventory
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = '__all__'
