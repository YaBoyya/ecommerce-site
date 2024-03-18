from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import ValidationError
from rest_framework.test import APIRequestFactory

from users.models import ECommerceUser
from users.serializers import (AuthSerializer,
                               ReviewSerializer,
                               UserAddressSerializer,
                               UserSerializer)


class TestUserSerializer(TestCase):
    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test',
        }

    def test_create_returns_correct_user(self):
        user = UserSerializer().create(self.data)
        self.assertEqual(self.data['username'], user.username)
        self.assertEqual(self.data['email'], user.email)

    def test_create_creates_useraddress(self):
        address = {
            'address_line1': 'test',
            'address_line2': 'test',
            'city': 'Test',
            'postal_code': '27',
            'country': 'Test',
            'telephone': None,
            'mobile': None
            }
        self.data.update({'address': address})

        user = UserSerializer().create(self.data)
        serializer = UserAddressSerializer(user.useraddress_set.first())

        address.pop('user')
        self.assertEqual(address, serializer.data)


class TestAuthSerializer(TestCase):
    def setUp(self):
        self.hasher = PBKDF2PasswordHasher()
        self.factory = APIRequestFactory()
        self.data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test'
        }
        self.user = ECommerceUser.objects.create_user(**self.data)
        self.serializer = AuthSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['username', 'password']))

    def test_username_field_content(self):
        self.assertEqual(
            self.serializer.data['username'],
            self.data['username']
            )

    def test_password_field_content(self):
        self.assertTrue(self.hasher.verify(
            self.data['password'],
            self.serializer.data['password']
        ))

    def test_validate_returns_user(self):
        serializer = AuthSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        self.assertEqual(user, self.user)

    def test_validate_wrong_credentials(self):
        wrong_data = self.data
        wrong_data.update({'username': 'wrong'})
        serializer = AuthSerializer(data=wrong_data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn(
            _('Unable to log in with provided credentials.'),
            list(map(str, serializer.errors['non_field_errors'])))

    def test_validate_missing_credentials(self):
        data = {
            "username": '',
            "password": None
        }
        serializer = AuthSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn(
            'This field may not be blank.',
            list(map(str, serializer.errors['username'])))
        self.assertIn(
            'This field may not be null.',
            list(map(str, serializer.errors['password'])))


class TestReviewSerializer(TestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.data = {
            'product': 1,
            'title': 'Test',
            'desc': 'testtest',
            'rating': 2
        }

    def test_validate_valid_rating(self):
        serializer = ReviewSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)

    def test_validate_invalid_rating(self):
        self.data.update({'rating': -1})
        serializer = ReviewSerializer(data=self.data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn(
            _('Invalid rating value, should be in range 1-5.'),
            list(map(str, serializer.errors['non_field_errors'])))

        self.data.update({'rating': 10})
        serializer = ReviewSerializer(data=self.data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn(
            _('Invalid rating value, should be in range 1-5.'),
            list(map(str, serializer.errors['non_field_errors'])))
