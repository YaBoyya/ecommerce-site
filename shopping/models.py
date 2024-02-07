from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseECommerceModel


class OrderDetails(BaseECommerceModel):
    user = models.ForeignKey('users.ECommerceUser',
                             on_delete=models.CASCADE,
                             null=True, blank=True)


class OrderItems(BaseECommerceModel):
    order = models.ForeignKey(OrderDetails,
                              related_name='order_items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)
