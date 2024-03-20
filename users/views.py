from django.contrib.auth import login
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _

from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from knox.views import LoginView as KnoxLoginView

from shopping.models import OrderDetails
from shopping.serializers import OrderDetailsSerializer
from users import serializers
from users.models import Review, Wishlist


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = serializers.AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        self.request.user.stripe_create_user()
        return self.request.user

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.stripe_update_user()


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderDetails.objects.filter(user=self.request.user)\
            .order_by('created_at')

    def get(self, request, format=None):
        history = self.get_queryset()
        serializer = OrderDetailsSerializer(history, many=True)
        return Response(serializer.data)


class ReviewView(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ReviewSerializer
    queryset = Review.objects.all()

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=request.user)
        except IntegrityError:
            msg = {'error':
                   _('Review duplicate from given user under this product.')}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class WishlistView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=request.user)
        except IntegrityError:
            msg = {'error':
                   'Wishlist duplicate from given user under this product.'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        wishlist = self.get_queryset()
        serializer = self.get_serializer(wishlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)
