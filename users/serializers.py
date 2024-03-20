from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import ECommerceUser, UserAddress, Review, Wishlist


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

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'title', 'desc', 'rating']

    def validate(self, attrs):
        rating = attrs['rating']

        if rating > 5 or rating < 1:
            msg = _('Invalid rating value, should be in range 1-5.')
            raise serializers.ValidationError(msg)
        return super().validate(attrs)


class WishlistSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Wishlist
        fields = ['product', 'created_at']
