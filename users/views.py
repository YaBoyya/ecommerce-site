from django.contrib.auth import login

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from knox.views import LoginView as KnoxLoginView

from shopping.models import OrderDetails
from shopping.serializers import OrderDetailsSerializer
from users.serializers import UserSerializer, AuthSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginView(KnoxLoginView):
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
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
