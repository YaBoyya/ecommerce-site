from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from core.models import ProductInventory
from shopping.models import OrderDetails, OrderItem


@receiver(post_save, sender=OrderItem)
@transaction.atomic
def update_product_inventory(sender, instance, created, **kwargs):
    if created:
        inventory = ProductInventory.objects.select_for_update()\
            .get(product=instance.product)

        inventory.quantity -= instance.quantity
        inventory.save()
    elif not created and\
            instance.order.status == OrderDetails.OrderStatus.CANCELED:
        inventory = ProductInventory.objects.select_for_update()\
            .get(product=instance.product)

        inventory.quantity += instance.quantity
        inventory.save()
    print(instance.order.status)


@receiver(pre_save, sender=OrderDetails)
@transaction.atomic
def revert_update_product_inventory(sender, instance, update_fields, **kwargs):
    order_status = OrderDetails.OrderStatus

    try:
        old_instance = sender.objects.get(id=instance.id)

        items = instance.items.all()

        if old_instance.status == order_status.OPEN\
                and instance.status == order_status.CANCELED:
            for item in items:
                inventory = ProductInventory.objects.select_for_update()\
                    .get(product=item.product)
                inventory.quantity += item.quantity
                inventory.save()
    except OrderDetails.DoesNotExist:
        pass
