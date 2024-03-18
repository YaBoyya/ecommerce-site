from django.test import TestCase
from django.core.exceptions import ValidationError

from stripe import Customer

from users.models import ECommerceUser, UserAddress


class TestECommerceUser(TestCase):
    def setUp(self):
        self.user = ECommerceUser.objects.create(
            username='test',
            email='test@example.com',
            password='test'
        )
        self.useraddress = UserAddress.objects.create(
            user=self.user,
            address_line1='Test street',
            address_line2='Test street 2',
            city='Test',
            postal_code='12345',
            country='JM',
            telephone='123456789'
        )

    def test_clean_valid(self):
        """Cleaning valid fields won't raise ValidationError"""
        self.user.full_clean()

    def test_clean_invalid(self):
        """Saving user with invalid email field will raise ValidationError"""
        self.user.email = 'test'
        with self.assertRaises(ValidationError):
            self.user.save()

    def test_save_valid(self):
        """Saving valid password won't raise ValidationError"""
        self.user.set_password('VeryHardPassword123')
        self.user.save()

    def test_save_invalid(self):
        """Saving invalid password will raise ValidationError"""
        self.user.set_password('test')
        with self.assertRaises(ValidationError):
            self.user.save()

    def test_stripe_create_user_valid_data(self):
        self.assertIsNone(self.user.stripe_id)
        self.user.stripe_create_user()
        self.assertIsNotNone(self.user.stripe_id)

    def test_stripe_create_user_invalid_data(self):
        user = ECommerceUser.objects.create(
            username='test1',
            email='test1@example.com',
            password='test'
        )
        self.assertIsNone(user.stripe_id)
        with self.assertRaises(AttributeError):
            user.stripe_create_user()
        self.assertIsNone(user.stripe_id)

    def test_stripe_update_user_valid_data(self):
        self.user.stripe_create_user()
        city = self.useraddress.city

        self.useraddress.city = 'Different City'
        self.useraddress.save()
        self.assertNotEqual(
            city,
            self.user.stripe_retrieve_user()['address']['city']
        )

    def test_delete_user(self):
        self.user.stripe_create_user()
        self.user.delete()
        self.assertTrue(self.user.stripe_retrieve_user()['deleted'])

    def test_get_name(self):
        self.assertIsNone(self.user.get_name())
        self.user.first_name = 'Test'
        self.user.last_name = 'Test'
        self.user.save()
        self.assertEqual(self.user.get_name(), 'Test Test')


class TestUserAddress(TestCase):
    def setUp(self):
        self.user = ECommerceUser.objects.create(
            username='test',
            email='test@example.com',
            password='test'
        )
        self.useraddress = UserAddress.objects.create(
            user=self.user,
            address_line1='Test street',
            address_line2='Test street 2',
            city='Test',
            postal_code='12345',
            country='JM',
            telephone='123456789'
        )

    def test_user_stripe_save(self):
        self.user.stripe_create_user()
        city = self.useraddress.city
        self.useraddress.city = 'Test-Test'
        self.useraddress.save()
        self.assertNotEqual(
            city,
            Customer.retrieve(self.user.stripe_id)['address']['city']
        )
