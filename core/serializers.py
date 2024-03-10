from rest_framework import serializers

from core import models


class FeedSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = [
            'name', 'category', 'rating',
            'inventory', 'price', 'discount'
        ]

    def get_category(self, obj):
        return obj.category.name

    def get_discount(self, obj):
        return {
            "discounted_price":
                round(
                    obj.price * (100 - obj.discount.discount_percent) / 100,
                    2
                ),
            "discount_percent": obj.discount.discount_percent
        } if obj.discount and obj.discount.is_active else None

    def get_inventory(self, obj):
        return obj.inventory.quantity

    def get_rating(self, obj):
        return obj.rating


class ProductSerializer(FeedSerializer):
    def get_category(self, obj):
        return {
            "name": obj.category.name,
            "desc": obj.category.desc
        }

    def get_discount(self, obj):
        return {
            "name": obj.discount.name,
            "desc": obj.discount.desc,
            "discount_percent": obj.discount.discount_percent,
            "discounted_price": round(
                obj.price * (100 - obj.discount.discount_percent) / 100,
                2)
        } if obj.discount and obj.discount.is_active else None


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
