from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.test import APITestCase

from knox.models import AuthToken

from core.models import Product
from shopping.models import OrderDetails
from users.models import ECommerceUser, Review, Wishlist


class TestLoginView(APITestCase):
    def setUp(self):
        self.url = reverse('users:knox_login')

    def test_login_valid(self):
        """User with valid login data should get logged in"""
        data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test'
        }
        self.user = ECommerceUser.objects.create_user(**data)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid(self):
        """User with invalid login data shouldn't get logged in"""
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
        self.data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test'
        }
        user = ECommerceUser.objects.create_user(**self.data)
        token = f"Token {AuthToken.objects.create(user=user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)
        self.url = reverse('users:profile')

    def test_user_profile_valid_token(self):
        """User with a valid token should get logged in"""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_invalid_token(self):
        """Only valid tokens should be allowed"""
        self.client.credentials(HTTP_AUTHORIZATION='invalid')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_change_email(self):
        """User should be able to change his email"""
        response = self.client.patch(self.url, {'email': 'newmail@gmail.com'})
        self.assertNotEqual(self.data['email'], response.data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_change_password(self):
        """User should be able to change password"""
        response = self.client.patch(self.url, {'password': 'NewPassword123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
        token = f"Token {AuthToken.objects.create(user=self.user1)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)
        self.url = reverse('users:history')
        OrderDetails.objects.create(user=self.user1, total='1')
        self.filtered = OrderDetails.objects.create(user=self.user2, total='1')

    def test_user_receives_history(self):
        """
        User history filters out all orders not related to user
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), len(self.user1.orders.all()))
        self.assertNotIn(self.filtered, response.data)


class TestReviewView(APITestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.url = reverse('users:review')
        self.user = ECommerceUser.objects.create_user(
            username='test',
            email='test@email.com',
            password='test')
        token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)
        self.data = {
            "product": 1,
            "title": "Test!",
            "desc": "TestTest",
            "rating": "5"
        }
        self.product = Product.objects.get(id=12)
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            title="Other Test",
            desc="This is a test",
            rating=2
        )
        self.details_url = reverse('users:review-details',
                                   kwargs={'pk': self.review.id})

    def test_post_unique_data(self):
        """Post method for unique data should create an item"""
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_duplicate_data(self):
        """Post method should not allow duplicate data"""
        self.client.post(self.url, data=self.data)
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            _('Review duplicate from given user under this product.'),
            response.data['error']
        )

    def test_delete(self):
        """Delete method should work correctly"""
        response = self.client.delete(self.details_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put(self):
        """Put method should work when updating whole item"""
        new_data = {
            'user': self.user.id,
            'product': self.product.id,
            'title': 'put',
            'desc': 'This is a test',
            'rating': '4'
        }
        response = self.client.put(self.details_url, new_data)
        self.assertNotEqual(response.data['title'], self.data['title'])
        self.assertNotEqual(response.data['rating'], self.data['rating'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        """Patch method should work for updating single field"""
        response = self.client.patch(self.details_url, {'title': 'patch'})
        self.assertNotEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWishlistView(APITestCase):
    fixtures = ['./fixtures/test_fixture.json']

    def setUp(self):
        self.url = reverse('users:wishlist')
        self.user = ECommerceUser.objects.create_user(
            username='test',
            email='test@email.com',
            password='test')
        token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)
        self.product = Product.objects.get(id=1)
        self.wishlist = Wishlist.objects.create(
            user=self.user,
            product=self.product
        )

    def test_post_unique_data(self):
        """Wishlist items should be created correctly"""
        data = {
            'user': self.user.id,
            'product': 2
        }
        response = self.client.post(self.url, data)
        self.assertEqual(data['product'], response.data['product'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_duplicate_data(self):
        """Duplicate wishlist items shouln't be allowed"""
        data = {
            'user': self.user.id,
            'product': self.product.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(
            response.data['error'],
            _('Wishlist duplicate from given user under this product.')
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_wishlist_list(self):
        """Wishlist should be listed correctly"""
        response = self.client.get(self.url)
        self.assertEqual(
            response.data['results'][0]['product'],
            self.product.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """Wishlist item under given pk should be deleted"""
        url_details = reverse(
            'users:wishlist-delete',
            kwargs={'pk': self.wishlist.id}
        )
        response = self.client.delete(url_details)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
