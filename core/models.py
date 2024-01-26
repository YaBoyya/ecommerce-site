from django.db import models
from django.db.models.signals import post_delete, pre_delete
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseECommerceModel(models.Model):
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), null=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        if self.pk:
            self.modified_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)


class ECommerceModel(BaseECommerceModel):
    deleted_at = models.DateTimeField(_('Deleted at'), default=None, null=True)

    class Meta:
        abstract = True

    def delete(self):
        pre_delete.send(sender=self.__class__, instance=self)
        self.deleted_at = timezone.now()
        post_delete.send(sender=self.__class__, instance=self)
        super().save()

    def _delete_no_signals(self):
        self.deleted_at = timezone.now()
        super().save()


class Product(ECommerceModel):
    name = models.CharField(_('Name'), max_length=150)
    desc = models.TextField(_('Description'), max_length=500)
    SKU = models.CharField(max_length=10)
    category = models.ForeignKey('core.ProductCategory', null=True,
                                 related_name='product',
                                 on_delete=models.SET_NULL)
    inventory = models.OneToOneField('core.ProductInventory', null=True,
                                     related_name='product',
                                     on_delete=models.CASCADE)
    price = models.FloatField(_('Price'))
    discount = models.ForeignKey('core.Discount', null=True,
                                 related_name='product',
                                 on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Products'


class ProductCategory(ECommerceModel):
    name = models.CharField(_('Name'), max_length=150)
    desc = models.TextField(_('Description'), max_length=500)

    class Meta:
        verbose_name_plural = 'ProductCategories'


class ProductInventory(ECommerceModel):
    quantity = models.IntegerField(_('Quantity'), default=0)

    class Meta:
        verbose_name_plural = 'ProductInvetories'


class Discount(ECommerceModel):
    name = models.CharField(_('Name'), max_length=150)
    desc = models.TextField(_('Description'), max_length=500)
    discount_percent = models.DecimalField(max_digits=3, decimal_places=0)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Discounts'
