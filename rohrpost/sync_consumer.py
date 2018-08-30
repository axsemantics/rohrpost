import json
from functools import partial

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from . import handlers
from .message import send_error
from .registry import HANDLERS

assert handlers  # silence qa

REQUIRED_FIELDS = ["type", "id"]

try:
    DECODE_ERRORS: tuple = (json.JSONDecodeError, TypeError)
except AttributeError:
    # Python 3.4 raises a ValueError instead of json.JSONDecodeError
    DECODE_ERRORS = (ValueError, TypeError)


class SyncRohrpostConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        """
        Handling of a rohrpost message will validate the required format:
        A valid JSON object including at least an "id" and "type" field.
        It then hands off further handling to the registered handler (if any).
        """
        _send_error = partial(send_error, consumer=self, message_id=None, handler=None)
        if not text_data:
            return _send_error(error="Received empty message.")

        try:
            request = json.loads(text_data)
        except DECODE_ERRORS as e:
            return _send_error(
                error="Could not decode JSON message. Error: {}".format(str(e))
            )

        if not isinstance(request, dict):
            return _send_error(error="Expected a JSON object as message.")

        for field in REQUIRED_FIELDS:
            if field not in request:
                return _send_error(error="Missing required field '{}'.".format(field))

        request_type = request["type"]
        if request_type not in HANDLERS:
            return send_error(
                consumer=self,
                message_id=request["id"],
                handler=request_type,
                error="Unknown message type '{}'.".format(request_type),
            )

        HANDLERS[request_type](consumer=self, request=request)

    def add_to_group(self, group_name) -> None:
        async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

    def remove_from_group(self, group_name) -> None:
        async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)
