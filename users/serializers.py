from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import ECommerceUser, UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'address_line1',
            'address_line2',
            'city',
            'postal_code',
            'country',
            'telephone',
            'mobile']


class UserSerializer(serializers.ModelSerializer):
    address = UserAddressSerializer(required=False)

    class Meta:
        model = ECommerceUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'address'
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        address = validated_data.pop('address', None)
        user = ECommerceUser.objects.create_user(**validated_data)
        if address:
            address.update({'user': user})
            UserAddress.objects.create(**address)
        return user


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
