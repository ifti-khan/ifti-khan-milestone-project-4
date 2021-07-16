# Importing two signal called post_save and post_delete,
# also importing a receiver for the signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Importing OrderLineItem to listen out for the signals
from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    This functions update order total on lineitem update/create
    using multiple signal arguments. Above the function is the
    executes command for the post_save signal using the receiver decorator
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete using multiple signal arguments.
    Above the function is the executes command for the post_delete
    signal using the receiver decorator
    """
    instance.order.update_total()
