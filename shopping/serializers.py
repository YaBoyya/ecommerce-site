from rest_framework import serializers

from shopping.models import CartItem, ShoppingSession


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class ShoppinSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingSession
        fields = '__all__'
        depth = 1
