from rohrpost.handlers import handle_ping


def test_ping(consumer):
    handle_ping(consumer=consumer, request={"id": 123})
    assert consumer.closed is False
    assert len(consumer.data) == 1

    data = consumer.data[-1]
    assert data["id"] == 123
    assert data["type"] == "pong"
    assert "data" not in data


def test_ping_additional_data(consumer):
    handle_ping(
        consumer=consumer,
        request={
            "id": 123,
            "type": "ping",
            "data": {"some": "data", "other": "data", "handler": "foo"},
        },
    )
    assert consumer.closed is False
    assert len(consumer.data) == 1

    data = consumer.data[-1]
    assert data["id"] == 123
    assert data["type"] == "pong"
    assert data["data"]["some"] == "data"
    assert data["data"]["handler"] == "foo"


def test_ping_additional_non_dict_data(consumer):
    handle_ping(consumer=consumer, request={"id": 123, "type": "ping", "data": 1})
    assert consumer.closed is False
    assert len(consumer.data) == 1

    data = consumer.data[-1]
    assert data["id"] == 123
    assert data["type"] == "pong"
    assert data["data"]["data"] == 1
