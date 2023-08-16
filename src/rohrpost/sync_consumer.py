import json
from typing import Any, Optional, Set, Union

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .main import handle_rohrpost_message
from .message import TolerantJSONEncoder


class SyncRohrpostConsumer(WebsocketConsumer):
    json_encoder = TolerantJSONEncoder

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._subscribed_groups: Set[str] = set()

    def connect(self) -> None:
        self.accept()

    def disconnect(self, code: Any) -> None:
        for group_name in list(self._subscribed_groups):
            self._subscribed_groups.remove(group_name)
            async_to_sync(self.channel_layer.group_discard)(
                group_name, self.channel_name
            )
        super().disconnect(code)

    def receive(
        self, text_data: Optional[str] = None, bytes_data: Optional[bytes] = None
    ) -> None:
        handle_rohrpost_message(consumer=self, text_data=text_data)

    def rohrpost_message(self, event: dict) -> None:
        """Send a message that was sent over a channel layer to the client.

        This expects an event as dict with a key `message` that contains the
        message that should be sent to the client.  The message can either be
        a string or a dict.

        For further information see
        https://channels.readthedocs.io/en/latest/topics/channel_layers.html#what-to-send-over-the-channel-layer
        """
        # Send a message down to the client
        message: Union[str, dict] = event["message"]
        if not isinstance(message, str):
            message = json.dumps(message, cls=self.json_encoder)
        self.send(text_data=message)

    def add_to_group(self, group_name: str) -> None:
        if group_name in self._subscribed_groups:
            return
        self._subscribed_groups.add(group_name)
        async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

    def remove_from_group(self, group_name: str) -> None:
        try:
            self._subscribed_groups.remove(group_name)
        except KeyError:
            return
        async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)
