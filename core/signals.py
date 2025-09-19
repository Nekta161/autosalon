from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .telegram import send_telegram_message


@receiver(post_save, sender=Order)
def notify_admin_on_new_order(sender, instance, created, **kwargs):
    if created:
        message = (
            f"🚨 *Новая заявка!*\n"
            f"ID: `{instance.id}`\n"
            f"Пользователь: `{instance.user.username}`\n"
            f"Авто: `{instance.car.brand} {instance.car.model}`\n"
            f"Цена: `{instance.car.price} ₽`\n"
            f"Статус: `{instance.get_status_display()}`\n"
            f"Создана: `{instance.created_at.strftime('%Y-%m-%d %H:%M')}`"
        )

        # Отправляем ВСЕГДА
        send_telegram_message(message)

        # WebSocket-уведомление
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "admin_notifications",
            {
                "type": "new_order",
                "order_id": instance.id,
                "car": str(instance.car),
                "user": instance.user.username,
                "created_at": instance.created_at.isoformat(),
            },
        )
