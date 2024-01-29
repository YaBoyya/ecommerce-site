from django.contrib.auth import login

from rest_framework import generics
from rest_framework.permissions import AllowAny

from knox.views import LoginView as KnoxLoginView

from users.serializers import UserSerializer, AuthSerializer


# TODO setup a viewset for this
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

    def get_object(self):
        return self.request.user
