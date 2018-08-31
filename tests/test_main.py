import json

from rohrpost.main import handle_rohrpost_message


def test_handle_empty_message(consumer):
    handle_rohrpost_message(consumer=consumer, text_data=None)

    assert len(consumer.data) == 1
    print("DEBUG", consumer.data)
    assert consumer.data[-1]["error"].startswith("Received empty message")


def test_handle_non_json(consumer):
    message = [1, 2, 3]
    handle_rohrpost_message(consumer=consumer, text_data=message)

    assert len(consumer.data) == 1
    assert consumer.data[-1]["error"].startswith("Could not decode JSON message")


def test_handle_nondict_message(consumer):
    message = json.dumps([1, 2, 3])
    handle_rohrpost_message(consumer=consumer, text_data=message)

    assert len(consumer.data) == 1
    assert consumer.data[-1]["error"].startswith("Expected a JSON object as message.")


def test_handle_missing_fields(consumer):
    message = json.dumps({})
    handle_rohrpost_message(consumer=consumer, text_data=message)

    assert len(consumer.data) == 1
    assert consumer.data[-1]["error"].startswith("Missing required field 'type'.")


def test_handle_unknown_type(consumer):
    message = json.dumps({"id": 123, "type": "handler_not_known"})
    handle_rohrpost_message(consumer=consumer, text_data=message)

    assert len(consumer.data) == 1
    assert consumer.data[-1]["error"].startswith("Unknown message type")


def test_successful_handle(consumer):
    message = json.dumps({"id": 123, "type": "ping"})
    handle_rohrpost_message(consumer=consumer, text_data=message)

    assert len(consumer.data) == 1
    assert consumer.data[-1]["type"] == "pong"


def test_successful_handle_zero_id(consumer):
    message = json.dumps({"id": 0, "type": "ping"})
    handle_rohrpost_message(consumer=consumer, text_data=message)

    assert len(consumer.data) == 1
    assert consumer.data[-1]["type"] == "pong"
