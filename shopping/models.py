from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseECommerceModel


class OrderDetails(BaseECommerceModel):
    class OrderStatus(models.TextChoices):
        ARCHIVED = ('ARCHIVED', _('archived'))
        CANCELED = ('CANCELED', _('canceled'))
        FULFILLED = ('FULFILLED', _('fulfilled'))
        OPEN = ('OPEN', _('open'))

    user = models.ForeignKey('users.ECommerceUser',
                             related_name='orders',
                             on_delete=models.CASCADE,
                             null=True, blank=True)
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2)
    status = models.CharField(_('status'),
                              choices=OrderStatus.choices,
                              default=OrderStatus.OPEN)

    class Meta:
        verbose_name_plural = 'OrderDetails'


class OrderItem(BaseECommerceModel):
    order = models.ForeignKey(OrderDetails,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)


class Payment(BaseECommerceModel):
    class CurrencyOptions(models.TextChoices):
        EUR = ('EUR', 'eur')
        PLN = ('PLN', 'pln')
        USD = ('USD', 'usd')

    class PaymentStatus(models.TextChoices):
        CANCELED = ('CANCELED', _('canceled'))
        FAILED = ('FAILED', _('failed'))
        PENDING = ('PENDING', _('pending'))
        SUCCEEDED = ('SUCCEEDED', _('succeeded'))

    class PaymentMethod(models.TextChoices):
        BLIK = ('BLIK', 'blik')
        CARD = ('CARD', 'card')

    order = models.OneToOneField(OrderDetails,
                                 related_name='payment',
                                 on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=9,
                                 decimal_places=2)
    currency = models.CharField(max_length=100,
                                choices=CurrencyOptions.choices)
    status = models.CharField(max_length=100,
                              choices=PaymentStatus.choices,
                              default=PaymentStatus.PENDING)
    method = models.CharField(max_length=100,
                              choices=PaymentMethod.choices)
