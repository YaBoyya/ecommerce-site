from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer


# TODO add filtration/ordering
class IndexView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer


# TODO restrict to only staff members
class ProductManagement(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
