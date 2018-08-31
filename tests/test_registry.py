import pytest

from rohrpost.registry import HANDLERS, rohrpost_handler


def test_register_entry():
    @rohrpost_handler("test-handler")
    def test_handler():
        return "test_handler called"

    assert "test-handler" in HANDLERS
    assert HANDLERS["test-handler"]() == "test_handler called"


def test_register_multiple_entries():
    @rohrpost_handler(["test-handler1", "test-handler2"])
    def test_handler():
        return "test_handler called"

    assert "test-handler1" in HANDLERS
    assert HANDLERS["test-handler1"]() == "test_handler called"
    assert HANDLERS["test-handler2"]() == "test_handler called"


def test_duplicate_entries():
    with pytest.raises(Exception) as exception_info:

        @rohrpost_handler("ping")
        def duplicate_ping_definition():
            pass

    assert str(exception_info.value).startswith('Handler for "ping" is already defined')
