from django.urls import re_path

from app.consumers import PublicAlertConsumer


websocket_urlpatterns = [
    re_path(r'ws/public_alerts/', PublicAlertConsumer.as_asgi()),  # конечная точка WebSocket
]
