from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseECommerceModel


class OrderDetails(BaseECommerceModel):
    user = models.ForeignKey('users.ECommerceUser',
                             on_delete=models.CASCADE,
                             null=True, blank=True)

    class Meta:
        verbose_name_plural = 'OrderDetails'


class OrderItem(BaseECommerceModel):
    order = models.ForeignKey(OrderDetails,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)
