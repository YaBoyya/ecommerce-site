from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Product, ProductInventory


@receiver(post_delete, sender=Product)
def delete_product_inventory(sender, instance, **kwargs):
    if instance.inventory:
        instance.inventory._delete_no_signals()


@receiver(post_delete, sender=ProductInventory)
def delete_product(sender, instance, **kwargs):
    if instance.product:
        instance.product._delete_no_signals()
