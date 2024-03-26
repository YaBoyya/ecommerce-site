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
        self.user_address = UserAddress.objects.create(
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

    def test_get_name(self):
        """get_name method returns None when there are no credentials
           and first_name second_name when they are not None"""
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
        self.user_address = UserAddress.objects.create(
            user=self.user,
            address_line1='Test street',
            address_line2='Test street 2',
            city='Test',
            postal_code='12345',
            country='JM',
            telephone='123456789'
        )

    def test_useraddress_stripe_save(self):
        """save methods updates stripe account accordingly"""
        self.user_address.stripe_create_user()
        city = self.user_address.city
        self.user_address.city = 'Test-Test'
        self.user_address.save()
        self.assertNotEqual(
            city,
            Customer.retrieve(self.user_address.stripe_id)['address']['city']
        )

    def test_stripe_create_customer_valid_data(self):
        """Stripe create method creates customer correctly with valid data"""
        self.assertIsNone(self.user_address.stripe_id)
        self.user_address.stripe_create_user()
        self.assertIsNotNone(self.user_address.stripe_id)

    def test_stripe_update_customer_valid_data(self):
        """Stripe update method updates customer correctly with valid data"""
        self.user_address.stripe_create_user()
        city = self.user_address.city

        self.user_address.city = 'Different City'
        self.user_address.save()
        self.assertNotEqual(
            city,
            self.user_address.stripe_retrieve_user()['address']['city']
        )

    def test_delete_useraddress(self):
        """When user_address account is deleted,
           stripe customer is deleted accordingly"""
        self.user_address.stripe_create_user()
        self.user_address.delete()
        self.assertTrue(
            self.user_address.stripe_retrieve_user()['deleted'])
