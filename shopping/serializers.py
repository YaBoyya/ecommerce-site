from django.db.models import F, Sum
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from shopping.models import OrderItem, OrderDetails, Payment


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = OrderDetails
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'product']

    # Update if there will be a need for creating singular item
    def create(self, validated_data):
        for item in validated_data:
            OrderItem.objects.create(**item)


class CartDetailsSerializer(serializers.ModelSerializer):
    total = ReadWriteSerializerMethodField(required=False)
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

    def get_total(self, obj):
        """
            Returns total cost of cart items
            When reading obj is an OrderedDict,
            but when writing it is a QuerySet
        """
        total = 0

        try:
            items = obj['items']
            for item in items:
                total += item['quantity'] * item['product'].price
        except TypeError:
            items = obj.items.all()
            total = items.aggregate(
                total=Sum(F('quantity') * F('product__price'))).get('total')

        return total


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
