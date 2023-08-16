import json
import random
import uuid
from collections.abc import Collection, Mapping
from decimal import Decimal
from typing import Any, Dict, Optional, Union

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

MessageID = Union[int, float, str, bytes]  # pylint: disable=invalid-name


class TolerantJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, Decimal):
            return int(o) if int(o) == o else float(o)
        if isinstance(o, Mapping):
            return dict(o)
        if isinstance(o, Collection):
            return list(o)
        return json.JSONEncoder.default(self, o)


def send_to_group(group_name: str, message: Union[str, dict]) -> None:
    """Send a message to a group.

    This requires the group to be exist on the default channel layer.
    """
    if async_to_sync is None:
        return
    async_to_sync(get_channel_layer().group_send)(
        group_name, {"type": "rohrpost.message", "message": message}
    )


def _send_message(*, consumer: WebsocketConsumer, content: dict) -> None:
    consumer.send(json.dumps(content, cls=TolerantJSONEncoder))


def build_message(
    *,
    handler: str,
    message_id: Optional[MessageID] = None,
    error: Optional[str] = None,
    generate_id: bool = False,
    data: Optional[dict] = None,
) -> dict:
    content: Dict[str, Union[MessageID, dict]] = {}
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
    message_id: Optional[MessageID] = None,
    error: Optional[str] = None,
    data: Optional[dict] = None,
) -> None:
    content = build_message(
        handler=handler, message_id=message_id, error=error, data=data
    )

    if not content:
        raise ValueError("Cannot send an empty message.")
    _send_message(consumer=consumer, content=content)


def send_success(
    *,
    consumer: WebsocketConsumer,
    handler: str,
    message_id: MessageID,
    data: Optional[dict] = None,
) -> None:
    """
    This method directly wraps send_message but checks the existence of id and type.
    """
    if message_id is None or handler is None:
        raise ValueError(
            "You have to provide a message ID and handler on success messages."
        )

    send_message(consumer=consumer, message_id=message_id, handler=handler, data=data)


def send_error(
    *,
    consumer: WebsocketConsumer,
    handler: str,
    message_id: MessageID,
    error: str,
    data: Optional[dict] = None,
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
