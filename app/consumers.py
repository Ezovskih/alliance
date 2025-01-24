from json import loads, dumps

from channels.generic.websocket import AsyncWebsocketConsumer

import redis.asyncio as aioredis


class MessageConsumer(AsyncWebsocketConsumer):
    user = None
    group_name = "public_group"

    @property
    def group_key(self):
        return f"{self.channel_layer.prefix}:group:{self.group_name}".encode("utf8")

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}_queue"  # личная группа пользователя
            # Добавляем пользователя в группу
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()


    async def disconnect(self, close_code):
        # Выводим пользователя из группы
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def _fetch_user_message(self):
        # Повторно используемое подключение
        client = aioredis.from_url('redis://127.0.0.1', encoding='utf-8', decode_responses=True)

        message = await client.lpop(self.group_key)

        await client.aclose()
        return loads(message) if message else None

    async def receive(self, text_data=None, bytes_data=None):
        data = loads(text_data)
        action = data.get('action')

        if action == 'get_message':
            # Запросить новое сообщение для пользователя
            message = await self._fetch_user_message()
            if message:
                # Отправляем клиенту сообщение
                await self.send(text_data=dumps({
                    'text': message.text,
                    'link': message.link,
                }))

    async def _post_user_message(self, text, link=None):
        # Повторно используемое подключение
        client = aioredis.from_url('redis://127.0.0.1')

        await client.delete(self.group_key)

        message = {'text': text, 'link': link}
        await client.rpush(self.group_key, dumps(message))

        await client.aclose()

    async def send_message(self, event):
        await self._post_user_message(event['text'], event['link'])
