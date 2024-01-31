from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseECommerceModel


class ShoppingSession(BaseECommerceModel):
    user = models.OneToOneField('users.ECommerceUser',
                                on_delete=models.CASCADE)
    total = models.DecimalField(_('total'), max_digits=5, decimal_places=2)


class CartItem(BaseECommerceModel):
    session = models.ForeignKey(ShoppingSession,
                                related_name='cart_item',
                                on_delete=models.CASCADE)
    product = models.OneToOneField('core.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)
