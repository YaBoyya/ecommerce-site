from django.db import models
from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phone_field.models import PhoneField

from core.models import BaseECommerceModel, ECommerceModel


# TODO add oauth2
class ECommerceUser(BaseECommerceModel, AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        if self._password is not None:
            password_validation.validate_password(self._password, self)
            password_validation.password_changed(self._password, self)
            self._password = None
        super().save(*args, **kwargs)


# TODO make it updatable
class UserAddress(models.Model):
    user = models.ForeignKey(ECommerceUser, on_delete=models.CASCADE)
    address_line1 = models.CharField(_('address 1'), max_length=300,
                                     blank=True)
    address_line2 = models.CharField(_('address 2'), max_length=300,
                                     blank=True)
    city = models.CharField(_('city'), max_length=150, blank=True)
    postal_code = models.CharField(_('post code'), max_length=50, blank=True)
    country = models.CharField(_('country'), max_length=150, blank=True)
    telephone = PhoneField(_('telephone'))
    mobile = PhoneField(_('mobile'))


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
                name="unique_product_review")
        ]
