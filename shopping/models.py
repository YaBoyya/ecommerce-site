from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseECommerceModel


class ShoppingSession(BaseECommerceModel):
    user = models.OneToOneField('users.ECommerceUser',
                                on_delete=models.CASCADE,
                                null=True, blank=True)


class CartItem(BaseECommerceModel):
    session = models.ForeignKey(ShoppingSession,
                                related_name='cart_items',
                                on_delete=models.CASCADE)
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)
