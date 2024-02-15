from django.db.models import Sum

from rest_framework import serializers

from shopping.models import OrderItem, OrderDetails


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetails
        fields = '__all__'

    def get_total(self, obj):
        return OrderItem.objects.filter(order=obj)\
            .aggregate(total=Sum('product__price')).get('total')


class CartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    order = serializers.IntegerField()
    product = serializers.IntegerField()

    class Meta:
        fields = '__all__'


class CartDetailsSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total = serializers.FloatField()
    user = serializers.IntegerField()

    class Meta:
        fields = '__all__'
