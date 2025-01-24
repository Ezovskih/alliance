from django.urls import re_path

from app.consumers import MessageConsumer


websocket_urlpatterns = [
    re_path(r'ws/messages/', MessageConsumer.as_asgi()),
]
