import json
import random
from decimal import Decimal


class TolerantJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        import uuid

        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, Decimal):
            return int(obj) if int(obj) == obj else float(obj)
        return json.JSONDecoder.default(self, obj)


def _send_message(*, message, content: dict, close: bool):
    message.reply_channel.send(
        {"text": json.dumps(content, cls=TolerantJSONEncoder), "close": close}
    )


def build_message(
    *, handler, message_id=None, error=None, generate_id=False, data: dict = None
):
    content = dict()
    if message_id:
        content["id"] = message_id
    elif generate_id:
        content["id"] = random.randint(a=1, b=1000)

    if handler:
        content["type"] = handler
    if error:
        content["error"] = error
    if data:
        content["data"] = data
    return content


def send_message(
    *, message, handler, message_id=None, close=False, error=None, data: dict = None
):
    content = build_message(
        handler=handler, message_id=message_id, error=error, data=data
    )

    if not content:
        raise Exception("Cannot send an empty message.")
    _send_message(message=message, content=content, close=close)


def send_success(*, message, handler, message_id, close=False, data: dict = None):
    """
    This method directly wraps send_message but checks the existence of id and type.
    """
    if message_id is None or handler is None:
        raise Exception(
            "You have to provide a message ID and handler on success messages."
        )

    send_message(
        message=message, message_id=message_id, handler=handler, close=close, data=data
    )


def send_error(*, message, handler, message_id, error, close=False, data: dict = None):
    """
    This method wraps send_message and makes sure that error is a keyword argument.
    """
    send_message(
        message=message,
        message_id=message_id,
        handler=handler,
        error=error,
        close=close,
        data=data,
    )
