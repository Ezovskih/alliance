from json import dumps

from django.urls import reverse
from channels.generic.websocket import AsyncWebsocketConsumer


class PublicAlertConsumer(AsyncWebsocketConsumer):
    group_name = "public_alerts"

    async def connect(self):
        # Присоединяем пользователя к группе
        # TODO self.user_id = self.scope['user'].id
        #  self.group_name = f"user_{self.user_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Отключаем пользователя от группы
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_polygon_alert(self, event):
        await self.send(text_data=dumps({
            'message': event['message'],
            'url': reverse('polygon_update', args=(event['polygon_id'],)),
        }))
