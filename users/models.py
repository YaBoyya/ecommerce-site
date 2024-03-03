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


# TODO add oauth2
class ECommerceUser(BaseECommerceModel, AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    stripe_id = models.CharField(max_length=50, blank=True, null=True)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        if self._password is not None:
            password_validation.validate_password(self._password, self)
            password_validation.password_changed(self._password, self)
            self._password = None
        super().save(*args, **kwargs)

    def stripe_create_user(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        address = self.useraddress_set.first()
        customer = Customer.create(
            name=self.get_name(),
            email=self.email,
            address={
                "city": address.city,
                "country": address.country,
                "line1": address.address_line1,
                "postal_code": address.postal_code
            },
            phone=address.mobile if address.mobile else address.telephone
        )
        self.stripe_id = customer.id
        self.save()

    def stripe_update_user(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        address = self.useraddress_set.first()
        Customer.modify(
            id=self.stripe_id,
            name=self.get_name(),
            email=self.email,
            address={
                "city": address.city,
                "country": address.country,
                "line1": address.address_line1,
                "postal_code": address.postal_code
            },
            phone=address.mobile if address.mobile else address.telephone
        )
        self.save()

    def get_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None


class UserAddress(models.Model):
    user = models.ForeignKey(ECommerceUser, on_delete=models.CASCADE)
    address_line1 = models.CharField(_('address 1'), max_length=300,
                                     blank=True)
    address_line2 = models.CharField(_('address 2'), max_length=300,
                                     blank=True)
    city = models.CharField(_('city'), max_length=150, blank=True)
    postal_code = models.CharField(_('post code'), max_length=50, blank=True)
    country = models.CharField(_('country'), max_length=150, blank=True)
    telephone = PhoneField(_('telephone'), null=True, blank=True)
    mobile = PhoneField(_('mobile'), null=True, blank=True)


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
