from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    serializer_class = Product
    queryset = Product.objects.all()

    class Meta:
        model = Product
        fields = '__all__'
