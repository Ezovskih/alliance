from json import loads, dumps

from channels.generic.websocket import AsyncWebsocketConsumer

import redis.asyncio as aioredis

from app.settings import SERVER_IP


class MessageConsumer(AsyncWebsocketConsumer):
    user = None
    group_name = "public_group"

    @property
    def group_key(self):
        """Common function to make the storage key for the group."""
        return f"{self.channel_layer.prefix}:group:{self.group_name}"

    @property
    def user_queue(self):
        return self.get_user_queue(self.user.id)

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}_group"  # личная группа пользователя
            # Добавляем пользователя в группу
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Выводим пользователя из группы
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def _fetch_user_message(self) -> dict | None:
        # Повторно используемое подключение
        client = aioredis.from_url(f"redis://{SERVER_IP}", encoding='utf-8', decode_responses=True)

        # Ищем адресованное пользователю сообщение
        data = await client.lpop(self.user_queue)
        await client.aclose()

        if not data:
            return None
        try:
            message = loads(data)
        except ValueError:
            return { "text": data, "link": None }
        else:
            return message

    async def receive(self, text_data=None, bytes_data=None):
        data = loads(text_data)
        action = data.get('action')

        if action == 'get_message':
            message = await self._fetch_user_message()
            if message is not None:
                # Отправляем сообщение пользователю
                await self.send(text_data=dumps({
                    'text': message['text'],
                    'link': message['link'],
                }))

    @classmethod
    def get_user_queue(cls, user_id):
        return f"user_{user_id}_queue"

    @classmethod
    async def post_user_message(cls, queue, text, link=None):
        # Повторно используемое подключение
        client = aioredis.from_url(f"redis://{SERVER_IP}")

        message = {'text': text, 'link': link}
        await client.rpush(queue, dumps(message))

        await client.aclose()
