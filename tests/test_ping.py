from rohrpost.handlers import handle_ping


def test_ping(message):
    handle_ping(message, request={'id': 123})
    assert message.reply_channel.closed is False
    assert len(message.reply_channel.data) == 1

    data = message.reply_channel.data[-1]
    assert data['id'] == 123
    assert data['type'] == 'pong'
    assert 'data' not in data


def test_ping_additional_data(message):
    handle_ping(message, request={
        'id': 123,
        'type': 'ping',
        'data': {'some': 'data', 'other': 'data', 'handler': 'foo'}
    })
    assert message.reply_channel.closed is False
    assert len(message.reply_channel.data) == 1

    data = message.reply_channel.data[-1]
    assert data['id'] == 123
    assert data['type'] == 'pong'
    assert data['data']['some'] == 'data'
    assert data['data']['handler'] == 'foo'


def test_ping_additional_non_dict_data(message):
    handle_ping(message, request={
        'id': 123,
        'type': 'ping',
        'data': 1
    })
    assert message.reply_channel.closed is False
    assert len(message.reply_channel.data) == 1

    data = message.reply_channel.data[-1]
    assert data['id'] == 123
    assert data['type'] == 'pong'
    assert data['data']['data'] == 1
