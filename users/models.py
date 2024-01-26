from django.db import models
from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from phone_field.models import PhoneField

from core.models import BaseECommerceModel


class ECommerceUser(BaseECommerceModel, AbstractBaseUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_admin = models.BooleanField(_('admin status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    # TODO overwrite create_user methods and remove usernames,
    # and clean for email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None


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

