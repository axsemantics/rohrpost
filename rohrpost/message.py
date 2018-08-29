import json
import random
from decimal import Decimal


def deprecate(message):
    import warnings

    warnings.warn(message, DeprecationWarning, stacklevel=3)


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
    *,
    handler,
    message_id=None,
    error=None,
    generate_id=False,
    data: dict = None,
    **additional_data
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
    if data or additional_data:
        content["data"] = data or {}
        if additional_data:
            deprecate(
                "Passing arbitrary kwargs to `build_message()` is depreated."
                " Pass in a dict `data` instead."
            )
            content["data"].update(additional_data)
    return content


def send_message(
    *,
    message,
    handler,
    message_id=None,
    close=False,
    error=None,
    data: dict = None,
    **additional_data
):
    if additional_data:
        deprecate(
            "Passing arbitrary kwargs to `send_message()` is depreated."
            " Pass in a dict `data` instead."
        )
        if data is None:
            data = {}
        data.update(additional_data)
    content = build_message(
        handler=handler, message_id=message_id, error=error, data=data
    )

    if not content:
        raise Exception("Cannot send an empty message.")
    _send_message(message=message, content=content, close=close)


def send_success(
    *, message, handler, message_id, close=False, data: dict = None, **additional_data
):
    """
    This method directly wraps send_message but checks the existence of id and type.
    """
    if message_id is None or handler is None:
        raise Exception(
            "You have to provide a message ID and handler on success messages."
        )

    if additional_data:
        deprecate(
            "Passing arbitrary kwargs to `send_success()` is depreated."
            " Pass in a dict `data` instead."
        )
        if data is None:
            data = {}
        data.update(additional_data)

    send_message(
        message=message, message_id=message_id, handler=handler, close=close, data=data
    )


def send_error(
    *,
    message,
    handler,
    message_id,
    error,
    close=False,
    data: dict = None,
    **additional_data
):
    """
    This method wraps send_message and makes sure that error is a keyword argument.
    """
    if additional_data:
        deprecate(
            "Passing arbitrary kwargs to `send_error()` is depreated."
            " Pass in a dict `data` instead."
        )
        if data is None:
            data = {}
        data.update(additional_data)

    send_message(
        message=message,
        message_id=message_id,
        handler=handler,
        error=error,
        close=close,
        data=data,
    )
