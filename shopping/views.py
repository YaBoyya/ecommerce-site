from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from shopping.models import OrderDetails, OrderItems
from shopping.serializers import OrderDetailsSerializer, OrderItemsSerializer


class OrderDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return OrderDetails.objects.get_or_create(user=self.request.user)

    def get(self, request, format=None):
        session = self.get_object()[0]
        serializer = OrderDetailsSerializer(session)
        return Response(serializer.data)


# TODO Maybe change the url to something like product/<str:pk>/add
class OrderItemsViewSet(ModelViewSet):
    serializer_class = OrderItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItems.objects.filter(order__user=self.request.user)
# TODO check how ordering products without account is done
