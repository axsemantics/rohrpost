import pytest

from rohrpost.message import send_error, send_message, send_success


def test_send_error(message):
    send_error(message=message, message_id=1, handler='some_handler', error='error_message')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'
    assert data[0]['error'] == 'error_message'


def test_send_error_with_additional_data(message):
    send_error(message=message, message_id=1, handler='some_handler', error='error_message', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'
    assert data[0]['error'] == 'error_message'
    assert data[0]['data']['some_field'] == 'additional_info'


def test_send_error_without_id(message):
    send_error(message=message, message_id=None, handler='some_handler', error='error_message')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert data[0]['type'] == 'some_handler'
    assert data[0]['error'] == 'error_message'


def test_send_error_without_id_with_additional_data(message):
    send_error(message=message, message_id=None, handler='some_handler', error='error_message', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert data[0]['type'] == 'some_handler'
    assert data[0]['error'] == 'error_message'
    assert data[0]['data']['some_field'] == 'additional_info'


def test_send_error_without_id_and_type(message):
    send_error(message=message, message_id=None, handler=None, error='error_message', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert 'type' not in data[0]
    assert data[0]['error'] == 'error_message'
    assert data[0]['data']['some_field'] == 'additional_info'


def test_send_error_without_anything(message):
    send_error(message=message, message_id=None, handler=None, error='error_message')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert 'type' not in data[0]
    assert data[0]['error'] == 'error_message'


def test_send_success(message):
    send_success(message=message, message_id=1, handler='some_handler')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'


def test_send_success_with_additional_data(message):
    send_success(message=message, message_id=1, handler='some_handler', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'
    assert data[0]['data']['some_field'] == 'additional_info'
    assert 'some_field' not in data[0]


def test_send_success_without_id(message):
    with pytest.raises(Exception) as exc:
        send_success(message=message, message_id=None, handler='some_handler')
    assert 'ID and handler' in str(exc.value)


def test_send_success_without_id_with_additional_data(message):
    with pytest.raises(Exception) as exc:
        send_success(message=message, message_id=None, handler='some_handler', some_field='additional_info')
    assert 'ID and handler' in str(exc.value)


def test_send_success_without_id_and_type(message):
    with pytest.raises(Exception) as exc:
        send_success(message=message, message_id=None, handler=None, some_field='additional_info')
    assert 'ID and handler' in str(exc.value)


def test_send_message(message):
    send_message(message=message, message_id=1, handler='some_handler')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'


def test_send_message_with_additional_data(message):
    send_message(message=message, message_id=1, handler='some_handler', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'
    assert data[0]['data']['some_field'] == 'additional_info'


def test_send_message_without_id(message):
    send_message(message=message, message_id=None, handler='some_handler')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert data[0]['type'] == 'some_handler'


def test_send_message_without_id_with_additional_data(message):
    send_message(message=message, message_id=None, handler='some_handler', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert data[0]['type'] == 'some_handler'
    assert data[0]['data']['some_field'] == 'additional_info'


def test_send_message_without_id_and_type(message):
    send_message(message=message, message_id=None, handler=None, some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert 'type' not in data[0]
    assert data[0]['data']['some_field'] == 'additional_info'


def test_send_message_without_anything(message):
    with pytest.raises(Exception) as exc:
        send_message(message=message, message_id=None, handler=None)
    assert 'empty message' in str(exc.value)
