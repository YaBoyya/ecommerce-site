from django.test import TestCase
from django.contrib.auth.hashers import PBKDF2PasswordHasher

from rest_framework.serializers import ValidationError
from rest_framework.test import APIRequestFactory

from users.models import ECommerceUser
from users.serializers import AuthSerializer, UserSerializer


class TestUserSerializer(TestCase):
    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test'
        }

    def test_create_returns_correct_user(self):
        user = UserSerializer().create(self.data)
        self.assertEqual(self.data['username'], user.username)
        self.assertEqual(self.data['email'], user.email)


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
            'Unable to log in with provided credentials',
            list(map(str, serializer.errors['non_field_errors'])))
