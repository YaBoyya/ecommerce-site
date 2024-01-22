from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    desc = models.TextField(_('Description'), max_length=500)
    SKU = models.CharField(max_length=10)
    category_id = models.ForeignKey('core.ProductCategory', null=True,
                                    on_delete=models.SET_NULL)
    inventory_id = models.ForeignKey('core.ProductInventory', null=True,
                                     on_delete=models.SET_NULL)
    price = models.FloatField(_('Price'))
    discount_id = models.ForeignKey('core.Discount', null=True,
                                    on_delete=models.SET_NULL)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), auto_now_add=True)
    deleted_at = models.DateTimeField(_('Deleted at'), default=None, null=True)

    class Meta:
        verbose_name_plural = 'Products'


class ProductCategory(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    desc = models.TextField(_('Description'), max_length=500)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), auto_now_add=True)
    deleted_at = models.DateTimeField(_('Deleted at'), default=None, null=True)

    class Meta:
        verbose_name_plural = 'ProductCategories'


class ProductInventory(models.Model):
    quantity = models.IntegerField(_('Quantity'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), auto_now_add=True)
    deleted_at = models.DateTimeField(_('Deleted at'), default=None, null=True)

    class Meta:
        verbose_name_plural = 'ProductInvetories'


class Discount(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    desc = models.TextField(_('Description'), max_length=500)
    discount_percent = models.DecimalField(max_digits=3, decimal_places=0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), auto_now_add=True)
    deleted_at = models.DateTimeField(_('Deleted at'), default=None, null=True)

    class Meta:
        verbose_name_plural = 'Discounts'
