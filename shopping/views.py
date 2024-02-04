from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from shopping.models import ShoppingSession, CartItem
from shopping.serializers import ShoppingSessionSerializer, CartItemSerializer


class ShoppingSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return ShoppingSession.objects.get_or_create(user=self.request.user)

    def get(self, request, format=None):
        session = self.get_object()[0]
        serializer = ShoppingSessionSerializer(session)
        return Response(serializer.data)


# TODO Maybe change the url to something like product/<str:pk>/add
class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get_query(self):
        return CartItem.objects.filter(session__user=self.request.user)

    def get(self, request, format=None):
        items = self.get_query()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
# TODO check how ordering products without account is done
