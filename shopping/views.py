from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from shopping.models import OrderDetails, OrderItems
from shopping.serializers import OrderDetailsSerializer, OrderItemsSerializer


class OrderDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return OrderDetails.objects.filter(user=self.request.user)

    # TODO decide what it should show either list or latest order
    def get(self, request, format=None):
        session = self.get_object()
        serializer = OrderDetailsSerializer(session, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# TODO Maybe change the url to something like product/<str:pk>/add
class OrderItemsViewSet(ModelViewSet):
    serializer_class = OrderItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItems.objects.filter(order__user=self.request.user)
# TODO check how ordering products without account is done
