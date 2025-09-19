from django.urls import path
from . import views, consumers

urlpatterns = [
    path("", views.index, name="index"),
]

websocket_urlpatterns = [
    path("ws/chat/<int:car_id>/", consumers.ChatConsumer.as_asgi()),
    path("ws/notifications/", consumers.NotificationConsumer.as_asgi()),
    path("ws/cars/", consumers.CarConsumer.as_asgi()),
]
