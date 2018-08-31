import json

from rohrpost.main import handle_rohrpost_message


def test_handle_empty_message(message):
    message.content = {"text": None}
    handle_rohrpost_message(message)

    assert len(message.reply_channel.data) == 1
    assert message.reply_channel.data[-1]["error"].startswith("Received empty message")


def test_handle_non_json(message):
    message.content = {"text": [1, 2, 3]}
    handle_rohrpost_message(message)

    assert len(message.reply_channel.data) == 1
    assert message.reply_channel.data[-1]["error"].startswith(
        "Could not decode JSON message"
    )


def test_handle_nondict_message(message):
    message.content = {"text": json.dumps([1, 2, 3])}
    handle_rohrpost_message(message)

    assert len(message.reply_channel.data) == 1
    assert message.reply_channel.data[-1]["error"].startswith(
        "Expected a JSON object as message."
    )


def test_handle_missing_fields(message):
    message.content = {"text": json.dumps({})}
    handle_rohrpost_message(message)

    assert len(message.reply_channel.data) == 1
    assert message.reply_channel.data[-1]["error"].startswith(
        "Missing required field 'type'."
    )


def test_handle_unknown_type(message):
    message.content = {"text": json.dumps({"id": 123, "type": "handler_not_known"})}
    handle_rohrpost_message(message)

    assert len(message.reply_channel.data) == 1
    assert message.reply_channel.data[-1]["error"].startswith("Unknown message type")


def test_successful_handle(message):
    message.content = {"text": json.dumps({"id": 123, "type": "ping"})}
    handle_rohrpost_message(message)

    assert len(message.reply_channel.data) == 1
    assert message.reply_channel.data[-1]["type"] == "pong"


def test_successful_handle_zero_id(message):
    message.content = {"text": json.dumps({"id": 0, "type": "ping"})}
    handle_rohrpost_message(message)

    assert len(message.reply_channel.data) == 1
    assert message.reply_channel.data[-1]["type"] == "pong"
