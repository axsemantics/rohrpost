import json
from functools import partial

from . import handlers  # noqa
from .message import send_error
from .registry import HANDLERS

REQUIRED_FIELDS = ["type", "id"]


try:
    DECODE_ERRORS = (json.JSONDecodeError, TypeError)
except AttributeError:
    # Python 3.4 raises a ValueError instead of json.JSONDecodeError
    DECODE_ERRORS = (ValueError, TypeError)


def handle_rohrpost_message(message):
    """
    Handling of a rohrpost message will validate the required format:
    A valid JSON object including at least an "id" and "type" field.
    It then hands off further handling to the registered handler (if any).
    """
    _send_error = partial(send_error, message=message, message_id=None, handler=None)
    if not message.content["text"]:
        return _send_error(error="Received empty message.")

    try:
        request = json.loads(message.content["text"])
    except DECODE_ERRORS as e:
        return _send_error(
            error="Could not decode JSON message. Error: {}".format(str(e))
        )

    if not isinstance(request, dict):
        return _send_error(error="Expected a JSON object as message.")

    for field in REQUIRED_FIELDS:
        if field not in request:
            return _send_error(error="Missing required field '{}'.".format(field))

    if not request["type"] in HANDLERS:
        return send_error(
            message=message,
            message_id=request["id"],
            handler=request["type"],
            error="Unknown message type '{}'.".format(request["type"]),
        )

    HANDLERS[request["type"]](message, request)
