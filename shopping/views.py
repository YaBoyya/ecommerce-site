from django.core.cache import cache
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

import stripe

from shopping.models import OrderDetails, OrderItem, Payment
from shopping.serializers import (CartDetailsSerializer,
                                  OrderDetailsSerializer,
                                  OrderItemSerializer,
                                  PaymentSerializer)


def get_cart(id):
    data = cache.get(id)
    if not data:
        return Response({'error': 'No data assigned to the given key.'},
                        status=status.HTTP_204_NO_CONTENT)
    return data


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = get_cart(request.user.id)
        if isinstance(data, Response):
            return data

        serializer = CartDetailsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        cache.delete(request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        data = get_cart(request.user.id)
        if isinstance(data, Response):
            return data

        serializer = CartDetailsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CartDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cache.set(request.user.id, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        cache.delete(request.user.id)
        return Response(status=status.HTTP_200_OK)

    def put(self, request, format=None):
        serializer = CartDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_data = cache.get(request.user.id)
        cache.set(request.user.id, serializer.data)

        if old_data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderDetails.objects.filter(user=self.request.user,
                                           is_active=True)

    def get(self, request, format=None):
        session = self.get_queryset()
        serializer = OrderDetailsSerializer(session, many=True)
        return Response(serializer.data)


# TODO Maybe change the url to something like product/<str:pk>/add
class OrderItemsViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)
# TODO check how ordering products without account is done


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.stripe_id:
            try:
                request.user.stripe_create_user()
            except AttributeError:
                msg = {'missing_data': 'User is missing UserAddress data.'}
                return Response(msg,
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_dict = serializer.validated_data
        order = data_dict.get('order')

        if request.user.id != order.user.id:
            msg = {'error': 'This user is not the owner of this order.'}
            return Response(msg, status=status.HTTP_401_UNAUTHORIZED)

        data_dict.update({'amount': order.total})

        stripe.api_key = settings.STRIPE_SECRET_KEY
        response = self.stripe_card_payment(data_dict)

        data_dict.pop('token')

        if response['status'] == "succeeded":
            Payment.objects.update_or_create(
                **data_dict,
                defaults={'status': Payment.PaymentStatus.SUCCEEDED})
        else:
            Payment.objects.update_or_create(
                **data_dict,
                defaults=data_dict)

        return Response(response, status=response['http_status'])

    def stripe_card_payment(self, data_dict):
        try:
            payment_intent = stripe.PaymentIntent.create(
                payment_method_types=['card'],
                amount=int(data_dict["amount"]*100),
                currency=data_dict['currency'],
                customer=self.request.user.stripe_id,
                payment_method=data_dict['token'],
            )
            payment_confirm = stripe.PaymentIntent.confirm(
                payment_intent['id']
            )

            payment_intent_modified = stripe.PaymentIntent.retrieve(
                payment_intent['id'])

            if (payment_intent_modified
                    and payment_intent_modified['status'] == 'succeeded'):
                response = {
                    "http_status": status.HTTP_200_OK,
                    "status": payment_confirm.status,
                    "message": "Card Payment Success",
                }
            else:
                response = {
                    "http_status": status.HTTP_400_BAD_REQUEST,
                    "status": payment_confirm.status,
                    "message": "Card Payment Failed",
                }
        except stripe.StripeError as e:
            response = {
                "http_status": e.http_status,
                "status": "failed",
                "error": e.error
            }
        return response
