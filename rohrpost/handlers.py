from rohrpost.message import send_message
from rohrpost.registry import rohrpost_handler


@rohrpost_handler("ping")
def handle_ping(message, request):
    """
    Handles requests of this format ("data" being an optional attribute):
    {
        "id": 123,
        "type": "ping",
        "data": {
            "some": "data"
        },
    }
    Response (again, with "data" optional but the same as in the request):
    {
        "id": 123,
        "type": "pong",
        "data": {
            "some": "data"
        },
    }
    Caution: if the sent data is not a dict, it will be wrapped in an
    additional "data" object in the response.
    """
    response_kwargs = {
        "message": message,
        "message_id": request["id"],
        "handler": "pong",
    }
    if "data" in request:
        if isinstance(request["data"], dict):
            response_kwargs.update(request["data"])
        else:
            response_kwargs["data"] = request["data"]

    send_message(**response_kwargs)
