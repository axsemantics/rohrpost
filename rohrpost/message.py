import json
import random
from decimal import Decimal

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer


class TolerantJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        import uuid

        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, Decimal):
            return int(obj) if int(obj) == obj else float(obj)
        return json.JSONDecoder.default(self, obj)


def send_to_group(group_name: str, message: str) -> None:
    """Send a message to a group.

    This requires the group to be exist on the default channel layer.
    """
    if async_to_sync is None:
        return
    async_to_sync(get_channel_layer().send)(group_name, message)


def _send_message(*, consumer: WebsocketConsumer, content: dict) -> None:
    consumer.send(json.dumps(content, cls=TolerantJSONEncoder))


def build_message(
    *,
    handler: str,
    message_id=None,
    error=None,
    generate_id: bool = False,
    data: dict = None
) -> dict:
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
    *,
    consumer: WebsocketConsumer,
    handler: str,
    message_id=None,
    error=None,
    data: dict = None
) -> None:
    content = build_message(
        handler=handler, message_id=message_id, error=error, data=data
    )

    if not content:
        raise Exception("Cannot send an empty message.")
    _send_message(consumer=consumer, content=content)


def send_success(
    *, consumer: WebsocketConsumer, handler: str, message_id, data: dict = None
) -> None:
    """
    This method directly wraps send_message but checks the existence of id and type.
    """
    if message_id is None or handler is None:
        raise Exception(
            "You have to provide a message ID and handler on success messages."
        )

    send_message(consumer=consumer, message_id=message_id, handler=handler, data=data)


def send_error(
    *, consumer: WebsocketConsumer, handler: str, message_id, error, data: dict = None
) -> None:
    """
    This method wraps send_message and makes sure that error is a keyword argument.
    """
    send_message(
        consumer=consumer,
        message_id=message_id,
        handler=handler,
        error=error,
        data=data,
    )
