from django.db.models import Sum

from rest_framework import serializers

from shopping.models import CartItem, ShoppingSession


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class ShoppingSessionSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField('get_total')

    class Meta:
        model = ShoppingSession
        fields = '__all__'

    def get_total(self, obj):
        return CartItem.objects.filter(session=obj)\
            .aggregate(total=Sum('product__price'))
