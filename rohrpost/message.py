import json


def _send_message(message, content: dict, close: bool):
    message.reply_channel.send({
        'text': json.dumps(content),
        'close': close,
    })


def send_message(message, message_id, handler, close=False, **additional_data):
    content = dict()
    if message_id:
        content['id'] = message_id
    if handler:
        content['type'] = handler

    content.update(**additional_data)
    _send_message(message, content, close=close)


def send_success(message, message_id, handler, close=False, **additional_data):
    send_message(message, message_id, handler, close=close, success=True, **additional_data)


def send_error(message, message_id, handler, error, close=False, **additional_data):
    additional_data.update({'error': error})
    send_message(message, message_id, handler, close=close, **additional_data)
