from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import ECommerceUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECommerceUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        return ECommerceUser.objects.create_user(**validated_data)


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_style': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            if not user:
                msg = _('Unable to log in with provided credentials')
                raise serializers.ValidationError(msg, code='authentication')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
