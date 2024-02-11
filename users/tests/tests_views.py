from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import ECommerceUser


class TestLoginView(APITestCase):
    def setUp(self):
        self.url = reverse('users:knox_login')

    def test_login_valid(self):
        data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test'
        }
        self.user = ECommerceUser.objects.create_user(**data)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid(self):
        data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test'
        }
        self.user = ECommerceUser.objects.create_user(**data)
        data.update({'password': 'invalid'})
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestManageUserView(APITestCase):
    def setUp(self):
        login_url = reverse('users:knox_login')
        data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test'
        }
        ECommerceUser.objects.create_user(**data)
        response = self.client.post(login_url, data, format='json')
        self.token = f"Token {response.data['token']}"
        self.url = reverse('users:profile')

    def test_user_profile_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.url, ormat='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='invalid')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
