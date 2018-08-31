from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .main import handle_rohrpost_message


class SyncRohrpostConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data: str) -> None:
        handle_rohrpost_message(consumer=self, text_data=text_data)

    def add_to_group(self, group_name) -> None:
        async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

    def remove_from_group(self, group_name) -> None:
        async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)
