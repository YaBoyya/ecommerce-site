from django.db.models import Sum

from rest_framework import serializers

from shopping.models import OrderItems, OrderDetails


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    cart_items = OrderItemsSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField('get_total')

    class Meta:
        model = OrderDetails
        fields = '__all__'

    def get_total(self, obj):
        return OrderItems.objects.filter(order=obj)\
            .aggregate(total=Sum('product__price'))
