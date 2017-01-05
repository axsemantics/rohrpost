import json


def _send_message(message, content: dict, close: bool):
    message.reply_channel.send({
        'text': json.dumps(content),
        'close': close,
    })


def send_message(message, message_id, handler, close=False, error=None, **additional_data):
    content = dict()
    if message_id:
        content['id'] = message_id
    if handler:
        content['type'] = handler
    if error:
        content['error'] = error
    if additional_data:
        content['data'] = additional_data

    if not content:
        raise Exception('Cannot send an empty message.')
    _send_message(message, content, close=close)


def send_success(message, message_id, handler, close=False, **additional_data):
    """
    This method directly wraps send_message but checks the existence of id and type.
    """
    if not message_id or not handler:
        raise Exception('You have to provide a message ID and handler on success messages.')

    send_message(message, message_id, handler, close=close, **additional_data)


def send_error(message, message_id, handler, error, close=False, **additional_data):
    """
    This method wraps send_message and makes sure that error is a keyword argument.
    """
    send_message(message, message_id, handler, close=close, error=error, **additional_data)
