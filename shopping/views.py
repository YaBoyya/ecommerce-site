from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
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
class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(session__user=self.request.user)

# TODO add summation of price in shopping sess
# TODO check how ordering products without account is done
