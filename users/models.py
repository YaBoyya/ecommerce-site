from django.db import models
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from phone_field.models import PhoneField

import stripe
from stripe import Customer

from core.models import BaseECommerceModel, ECommerceModel


class ECommerceUser(BaseECommerceModel, AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    def clean_fields(self, exclude=None):
        self.email = self.__class__.objects.normalize_email(self.email)
        super().clean_fields(exclude=exclude)

    def save(self, *args, **kwargs):
        if self._password:
            password_validation.validate_password(self._password, self)
            password_validation.password_changed(self._password, self)
            self._password = None
        super().save(*args, **kwargs)

    def get_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None


class UserAddress(models.Model):
    user = models.OneToOneField(ECommerceUser,
                                related_name="user_address",
                                on_delete=models.CASCADE)
    address_line1 = models.CharField(_('address 1'), max_length=300,
                                     blank=True)
    address_line2 = models.CharField(_('address 2'), max_length=300,
                                     blank=True)
    city = models.CharField(_('city'), max_length=150, blank=True)
    postal_code = models.CharField(_('post code'), max_length=50, blank=True)
    country = models.CharField(_('country'), max_length=150, blank=True)
    telephone = PhoneField(_('telephone'), null=True, blank=True)
    mobile = PhoneField(_('mobile'), null=True, blank=True)
    stripe_id = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.stripe_id:
            self.stripe_update_user()

    def delete(self):
        if self.stripe_id:
            self.stripe_delete_user()
        super().delete()

    def stripe_create_user(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = Customer.create(
            name=self.user.get_name(),
            email=self.user.email,
            address={
                "city": self.city,
                "country": self.country,
                "line1": self.address_line1,
                "line2": self.address_line2,
                "postal_code": self.postal_code
            },
            phone=self.mobile if self.mobile else self.telephone
        )
        self.stripe_id = customer.id
        super().save()

    def stripe_update_user(self):
        if self.stripe_id:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            Customer.modify(
                id=self.stripe_id,
                name=self.user.get_name(),
                email=self.user.email,
                address={
                    "city": self.city,
                    "country": self.country,
                    "line1": self.address_line1,
                    "line2": self.address_line2,
                    "postal_code": self.postal_code
                },
                phone=self.mobile if self.mobile else self.telephone
            )
            super().save()

    def stripe_delete_user(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        Customer.delete(sid=self.stripe_id)

    def stripe_retrieve_user(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return Customer.retrieve(self.stripe_id)


class Review(ECommerceModel):
    user = models.ForeignKey(ECommerceUser, on_delete=models.CASCADE)
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=100)
    desc = models.TextField()
    rating = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "user",
                "product",
                name="unique_product_user_review")
        ]


class Wishlist(models.Model):
    user = models.ForeignKey(ECommerceUser, on_delete=models.CASCADE)
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "user",
                "product",
                name="unique_product_user_wishlist")
        ]
