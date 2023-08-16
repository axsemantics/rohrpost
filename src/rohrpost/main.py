import json
from functools import partial
from typing import Optional

from channels.generic.websocket import WebsocketConsumer

from . import handlers  # noqa: F401  # pylint: disable=unused-import
from .message import send_error
from .registry import HANDLERS

REQUIRED_FIELDS = ["type", "id"]


def handle_rohrpost_message(
    consumer: WebsocketConsumer, text_data: Optional[str]
) -> None:
    """
    Handling of a rohrpost message will validate the required format:
    A valid JSON object including at least an "id" and "type" field.
    It then hands off further handling to the registered handler (if any).
    """
    _send_error = partial(send_error, consumer=consumer, message_id=None, handler=None)
    if not text_data:
        _send_error(error="Received empty message.")
        return

    try:
        request = json.loads(text_data)  # type: dict
    except (json.JSONDecodeError, TypeError) as exc:
        _send_error(error=f"Could not decode JSON message. Error: {str(exc)}")
        return

    if not isinstance(request, dict):
        _send_error(error="Expected a JSON object as message.")
        return

    for field in REQUIRED_FIELDS:
        if field not in request:
            _send_error(error=f"Missing required field '{field}'.")
            return

    request_type = request["type"]
    if request_type not in HANDLERS:
        send_error(
            consumer=consumer,
            message_id=request["id"],
            handler=request_type,
            error=f"Unknown message type '{request_type}'.",
        )
        return

    HANDLERS[request_type](consumer=consumer, request=request)
