from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from knox.models import AuthToken

from shopping.models import OrderDetails
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
        data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test'
        }
        user = ECommerceUser.objects.create_user(**data)
        self.token = f"Token {AuthToken.objects.create(user=user)[-1]}"
        self.url = reverse('users:profile')

    def test_user_profile_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='invalid')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestOrderHistoryView(APITestCase):
    def setUp(self):
        self.user1 = ECommerceUser.objects.create_user(
            username='test1',
            email='test1@email.com',
            password='test1')
        self.user2 = ECommerceUser.objects.create_user(
            username='test2',
            email='test2@email.com',
            password='test2')
        self.token = f"Token {AuthToken.objects.create(user=self.user1)[-1]}"
        self.url = reverse('users:history')
        OrderDetails.objects.create(user=self.user1, total='1')
        self.filtered = OrderDetails.objects.create(user=self.user2, total='1')

    def test_user_receives_history(self):
        """
        User history filters out all orders not related to user
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), len(self.user1.orders.all()))
        self.assertNotIn(self.filtered, response.data)
