from rest_framework import serializers

from shopping.models import CartItem, ShoppingSession


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class ShoppingSessionSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingSession
        fields = '__all__'
