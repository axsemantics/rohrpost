from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .main import handle_rohrpost_message


class SyncRohrpostConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subscribed_groups = set()

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        for group_name in list(self._subscribed_groups):
            self._subscribed_groups.remove(group_name)
            async_to_sync(self.channel_layer.group_discard)(
                group_name, self.channel_name
            )
        super().disconnect(close_code)

    def receive(self, text_data: str) -> None:
        handle_rohrpost_message(consumer=self, text_data=text_data)

    def add_to_group(self, group_name) -> None:
        if group_name in self._subscribed_groups:
            return
        self._subscribed_groups.add(group_name)
        async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

    def remove_from_group(self, group_name) -> None:
        try:
            self._subscribed_groups.remove(group_name)
        except KeyError:
            return
        async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)
