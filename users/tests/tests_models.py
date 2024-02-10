from django.test import TestCase
from django.core.exceptions import ValidationError

from users.models import ECommerceUser


class ECommerceUserTest(TestCase):
    def test_clean_valid(self):
        """Cleaning valid fields won't raise ValidationError"""
        instance = ECommerceUser(
            username='test',
            email='test@example.com',
            password='test')

        instance.full_clean()

    def test_clean_invalid(self):
        """Cleaning invalid email field will raise ValidationError"""
        instance = ECommerceUser(
            username='test',
            email='test',
            password='test')

        with self.assertRaises(ValidationError):
            instance.full_clean()

    def test_save_valid(self):
        """Saving valid password won't raise ValidationError"""
        instance = ECommerceUser(
            username='test',
            email='test@example.com',
            password='test')
        instance.set_password('VeryHardPassword123')
        instance.save()

    def test_save_invalid(self):
        """Saving invalid password will raise ValidationError"""
        instance = ECommerceUser(
            username='test',
            email='test@example.com',
            password='test')
        instance.set_password('test')
        with self.assertRaises(ValidationError):
            instance.save()
