import json
from functools import partial

from channels.generic.websocket import WebsocketConsumer

from . import handlers  # noqa
from .message import send_error
from .registry import HANDLERS

REQUIRED_FIELDS = ["type", "id"]


def handle_rohrpost_message(consumer: WebsocketConsumer, text_data: str) -> None:
    """
    Handling of a rohrpost message will validate the required format:
    A valid JSON object including at least an "id" and "type" field.
    It then hands off further handling to the registered handler (if any).
    """
    _send_error = partial(send_error, consumer=consumer, message_id=None, handler=None)
    if not text_data:
        return _send_error(error="Received empty message.")

    try:
        request = json.loads(text_data)  # type: dict
    except (json.JSONDecodeError, TypeError) as e:
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
            consumer=consumer,
            message_id=request["id"],
            handler=request_type,
            error="Unknown message type '{}'.".format(request_type),
        )

    HANDLERS[request_type](consumer=consumer, request=request)
