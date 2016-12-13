def test_send_error(message):
    send_error(message, 1, 'some_handler', 'error_message')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'
    assert data[0]['error'] == 'error_message'


def test_send_error_with_additional_data(message):
    send_error(message, 1, 'some_handler', 'error_message', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'
    assert data[0]['error'] == 'error_message'
    assert data[0]['some_field'] == 'additional_info'


def test_send_error_without_id(message):
    send_error(message, None, 'some_handler', 'error_message')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert data[0]['type'] == 'some_handler'
    assert data[0]['error'] == 'error_message'


def test_send_error_without_id_with_additional_data(message):
    send_error(message, None, 'some_handler', 'error_message', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert data[0]['type'] == 'some_handler'
    assert data[0]['error'] == 'error_message'
    assert data[0]['some_field'] == 'additional_info'


def test_send_error_without_id_and_type(message):
    send_error(message, None, None, 'error_message', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert 'type' not in data[0]
    assert data[0]['error'] == 'error_message'
    assert data[0]['some_field'] == 'additional_info'


def test_send_error_without_anything(message):
    send_error(message, None, None, 'error_message')
    data = message.reply_channel.data
    assert len(data) == 1
    assert 'id' not in data[0]
    assert 'type' not in data[0]
    assert data[0]['error'] == 'error_message'


def test_send_success(message):
    send_success(message, 1, 'some_handler')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'
    assert data[0]['success'] is True


def test_send_success_with_additional_data(message):
    send_success(message, 1, 'some_handler', some_field='additional_info')
    data = message.reply_channel.data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['type'] == 'some_handler'
    assert data[0]['success'] is True
    assert data[0]['some_field'] == 'additional_info'


def test_send_success_without_id(message):
    with pytest.raises(Exception) as exc:
        send_success(message, None, 'some_handler')
    assert 'ID and handler' in str(exc.value)


def test_send_success_without_id_with_additional_data(message):
    with pytest.raises(Exception) as exc:
        send_success(message, None, 'some_handler', 'success_message', some_field='additional_info')
    assert 'ID and handler' in str(exc.value)


def test_send_success_without_id_and_type(message):
    with pytest.raises(Exception) as exc:
        send_success(message, None, None, 'success_message', some_field='additional_info')
    assert 'ID and handler' in str(exc.value)
