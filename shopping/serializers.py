from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from shopping.models import OrderItem, OrderDetails, Payment


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
        fields = ['id', 'items', 'total']
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        items = validated_data.pop('items', None)
        order = OrderDetails.objects.create(**validated_data)

        if items:
            [item.update({'order': order}) for item in items]
            CartItemSerializer().create(items)

        return order


class PaymentSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = Payment
        fields = [
            'order',
            'currency',
            'method',
            'token'
        ]
        extra_kwargs = {'order': {'validators': []}}

    def validate_order(self, obj):
        if not obj:
            msg = _("Order must be specified")
            raise serializers.ValidationError(msg)

        if (hasattr(obj, "payment") and
                obj.payment.status == Payment.PaymentStatus.SUCCEEDED):
            msg = _("This order already has a payment that succeeded.")
            raise serializers.ValidationError(msg)

        return obj
