from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ECommerceModel(models.Model):
    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        if self.pk:
            self.modified_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)

    def delete(self):
        self.deleted_at = timezone.now()
        super().save()


class Product(ECommerceModel):
    name = models.CharField(_('Name'), max_length=150)
    desc = models.TextField(_('Description'), max_length=500)
    SKU = models.CharField(max_length=10)
    category_id = models.ForeignKey('core.ProductCategory', null=True,
                                    on_delete=models.SET_NULL)
    inventory_id = models.OneToOneField('core.ProductInventory', null=True,
                                        on_delete=models.CASCADE)
    price = models.FloatField(_('Price'))
    discount_id = models.ForeignKey('core.Discount', null=True,
                                    on_delete=models.SET_NULL)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), null=True)
    deleted_at = models.DateTimeField(_('Deleted at'), default=None, null=True)

    class Meta:
        verbose_name_plural = 'Products'


class ProductCategory(ECommerceModel):
    name = models.CharField(_('Name'), max_length=150)
    desc = models.TextField(_('Description'), max_length=500)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), null=True)
    deleted_at = models.DateTimeField(_('Deleted at'), default=None, null=True)

    class Meta:
        verbose_name_plural = 'ProductCategories'


class ProductInventory(ECommerceModel):
    quantity = models.IntegerField(_('Quantity'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), null=True)
    deleted_at = models.DateTimeField(_('Deleted at'), default=None, null=True)

    class Meta:
        verbose_name_plural = 'ProductInvetories'


class Discount(ECommerceModel):
    name = models.CharField(_('Name'), max_length=150)
    desc = models.TextField(_('Description'), max_length=500)
    discount_percent = models.DecimalField(max_digits=3, decimal_places=0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), null=True)
    deleted_at = models.DateTimeField(_('Deleted at'), default=None, null=True)

    class Meta:
        verbose_name_plural = 'Discounts'
