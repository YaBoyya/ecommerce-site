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


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'product']

    # Update if there will be a need for creating singular item
    def create(self, validated_data):
        for item in validated_data:
            OrderItem.objects.create(**item)


class CartDetailsSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = OrderDetails
        fields = ['total', 'items']

    def create(self, validated_data):
        print('create', validated_data)
        items = validated_data.pop('items')
        order = OrderDetails.objects.create(**validated_data)
        print(items)

        if items:
            [item.update({'order': order}) for item in items]
            print(items)
            CartItemSerializer().create(items)

        return order
