# core/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import ChatMessage, Car, Order


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.car_id = self.scope["url_route"]["kwargs"]["car_id"]
        self.room_group_name = f"chat_{self.car_id}"

        # Присоединиться к группе чата
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Покинуть группу чата
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Не закрывать соединение принудительно — оно закроется само при закрытии вкладки

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        user = self.scope["user"]

        if not user.is_authenticated:
            return

        # Сохранить сообщение в БД
        chat_message = await self.save_message(user, message)

        # Отправить сообщение всем в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": user.username,
                "avatar": await self.get_user_avatar(user),
                "timestamp": chat_message.created_at.isoformat(),
            },
        )

    async def chat_message(self, event):
        # Отправить сообщение клиенту
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "username": event["username"],
                    "avatar": event["avatar"],
                    "timestamp": event["timestamp"],
                }
            )
        )

    @sync_to_async
    def save_message(self, user, message):
        # Найти администратора (первого суперпользователя)
        admin = User.objects.filter(is_superuser=True).first()
        car = Car.objects.get(id=self.car_id)
        return ChatMessage.objects.create(
            user=user, admin=admin, message=message, car=car
        )

    @sync_to_async
    def get_user_avatar(self, user):
        try:
            return user.profile.avatar.url if user.profile.avatar else None
        except:
            return None


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_staff:
            await self.close()
            return

        self.group_name = "admin_notifications"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def new_order(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "new_order",
                    "order_id": event["order_id"],
                    "car": event["car"],
                    "user": event["user"],
                    "created_at": event["created_at"],
                }
            )
        )


class CarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "car_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def car_updated(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "car_updated",
                    "car_id": event["car_id"],
                    "status": event["status"],
                    "price": str(event["price"]),
                }
            )
        )
