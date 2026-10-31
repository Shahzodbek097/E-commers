from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .tasks import send_telegram


@receiver(post_save, sender=Order)
def notify_admin(instance, created, **kwargs):
    if created:
        send_telegram.delay(
            order_id=instance.id,
            product_nomi=instance.product.nomi,
            nechta=instance.nechta,
            buyurtmachi_username=instance.buyurtmachi.username,
            phone_number=instance.phone_number
        )



