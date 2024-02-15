from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from shopping.models import OrderDetails, OrderItem
from shopping.serializers import (CartDetailsSerializer,
                                  OrderDetailsSerializer,
                                  OrderItemSerializer)


class CartDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        data = cache.get(request.user.id)
        if not data:
            return Response({'error': 'No data assigned to the given key.'},
                            status=status.HTTP_204_NO_CONTENT)

        serializer = CartDetailsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        data.update({'user': request.user.id})

        serializer = CartDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cache.set(request.user.id, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderDetails.objects.filter(user=self.request.user)

    # TODO decide what it should show either list or latest order
    def get(self, request, format=None):
        session = self.get_queryset()
        serializer = OrderDetailsSerializer(session, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# TODO Maybe change the url to something like product/<str:pk>/add
class OrderItemsViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)
# TODO check how ordering products without account is done
