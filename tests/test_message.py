import decimal
import uuid
from collections import UserDict, UserList

import pytest

from rohrpost.message import TolerantJSONEncoder, send_error, send_message, send_success


def test_send_error(consumer):
    send_error(
        consumer=consumer, message_id=1, handler="some_handler", error="error_message"
    )
    data = consumer.data
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["type"] == "some_handler"
    assert data[0]["error"] == "error_message"


def test_send_error_with_additional_data(consumer):
    send_error(
        consumer=consumer,
        message_id=1,
        handler="some_handler",
        error="error_message",
        data={"some_field": "additional_info"},
    )
    data = consumer.data
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["type"] == "some_handler"
    assert data[0]["error"] == "error_message"
    assert data[0]["data"]["some_field"] == "additional_info"


def test_send_error_without_id(consumer):
    send_error(
        consumer=consumer,
        message_id=None,
        handler="some_handler",
        error="error_message",
    )
    data = consumer.data
    assert len(data) == 1
    assert "id" not in data[0]
    assert data[0]["type"] == "some_handler"
    assert data[0]["error"] == "error_message"


def test_send_error_without_id_with_additional_data(consumer):
    send_error(
        consumer=consumer,
        message_id=None,
        handler="some_handler",
        error="error_message",
        data={"some_field": "additional_info"},
    )
    data = consumer.data
    assert len(data) == 1
    assert "id" not in data[0]
    assert data[0]["type"] == "some_handler"
    assert data[0]["error"] == "error_message"
    assert data[0]["data"]["some_field"] == "additional_info"


def test_send_error_without_id_and_type(consumer):
    send_error(
        consumer=consumer,
        message_id=None,
        handler=None,
        error="error_message",
        data={"some_field": "additional_info"},
    )
    data = consumer.data
    assert len(data) == 1
    assert "id" not in data[0]
    assert "type" not in data[0]
    assert data[0]["error"] == "error_message"
    assert data[0]["data"]["some_field"] == "additional_info"


def test_send_error_without_anything(consumer):
    send_error(consumer=consumer, message_id=None, handler=None, error="error_message")
    data = consumer.data
    assert len(data) == 1
    assert "id" not in data[0]
    assert "type" not in data[0]
    assert data[0]["error"] == "error_message"


def test_send_success(consumer):
    send_success(consumer=consumer, message_id=1, handler="some_handler")
    data = consumer.data
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["type"] == "some_handler"


def test_send_success_with_additional_data(consumer):
    send_success(
        consumer=consumer,
        message_id=1,
        handler="some_handler",
        data={"some_field": "additional_info"},
    )
    data = consumer.data
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["type"] == "some_handler"
    assert data[0]["data"]["some_field"] == "additional_info"
    assert "some_field" not in data[0]


def test_send_success_without_id(consumer):
    with pytest.raises(Exception) as exc:
        send_success(consumer=consumer, message_id=None, handler="some_handler")
    assert "ID and handler" in str(exc.value)


def test_send_success_without_id_with_additional_data(consumer):
    with pytest.raises(Exception) as exc:
        send_success(
            consumer=consumer,
            message_id=None,
            handler="some_handler",
            data={"some_field": "additional_info"},
        )
    assert "ID and handler" in str(exc.value)


def test_send_success_without_id_and_type(consumer):
    with pytest.raises(Exception) as exc:
        send_success(
            consumer=consumer,
            message_id=None,
            handler=None,
            data={"some_field": "additional_info"},
        )
    assert "ID and handler" in str(exc.value)


def test_send_message(consumer):
    send_message(consumer=consumer, message_id=1, handler="some_handler")
    data = consumer.data
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["type"] == "some_handler"


def test_send_message_with_additional_data(consumer):
    send_message(
        consumer=consumer,
        message_id=1,
        handler="some_handler",
        data={"some_field": "additional_info"},
    )
    data = consumer.data
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["type"] == "some_handler"
    assert data[0]["data"]["some_field"] == "additional_info"


def test_send_message_without_id(consumer):
    send_message(consumer=consumer, message_id=None, handler="some_handler")
    data = consumer.data
    assert len(data) == 1
    assert "id" not in data[0]
    assert data[0]["type"] == "some_handler"


def test_send_message_without_id_with_additional_data(consumer):
    send_message(
        consumer=consumer,
        message_id=None,
        handler="some_handler",
        data={"some_field": "additional_info"},
    )
    data = consumer.data
    assert len(data) == 1
    assert "id" not in data[0]
    assert data[0]["type"] == "some_handler"
    assert data[0]["data"]["some_field"] == "additional_info"


def test_send_message_without_id_and_type(consumer):
    send_message(
        consumer=consumer,
        message_id=None,
        handler=None,
        data={"some_field": "additional_info"},
    )
    data = consumer.data
    assert len(data) == 1
    assert "id" not in data[0]
    assert "type" not in data[0]
    assert data[0]["data"]["some_field"] == "additional_info"


def test_send_message_without_anything(consumer):
    with pytest.raises(Exception) as exc:
        send_message(consumer=consumer, message_id=None, handler=None)
    assert "empty message" in str(exc.value)


@pytest.mark.parametrize(
    "item, expected",
    [
        (
            uuid.UUID("3265e5a9-29bf-4fce-af93-7fc04cdb1e7b"),
            '"3265e5a9-29bf-4fce-af93-7fc04cdb1e7b"',
        ),
        (decimal.Decimal(3), "3"),
        (decimal.Decimal(3.2), "3.2"),
        (UserDict(), "{}"),
        (UserList(), "[]"),
        (frozenset(), "[]"),
    ],
)
def test_tolerant_json_encoder(item, expected):
    assert TolerantJSONEncoder().encode(item) == expected
