rohrpost
========

**`rohrpost` is still very much a WIP project. Its interface and structure may still be subject
to unpredictable changes.**

`rohrpost` is a simple WebSocket protocol. It is designed to work with Django_ using Channels_ but
will interface with every base service implementing the ASGI_ specification (which, at the moment,
is mostly Channels_ with Daphne_).

The client implementation is rohrpost-js_.

Protocol
--------

The `rohrpost` protocol is very simple. The client may send messages containing an `id` (integer),
a `type` (string), and an optional data field (any JSON type):

.. code:: JSON

    {
        "id": 123,
        "type": "ping",
        "data": "something",
    }

The server will (if the mandatory fields have been sent) try to give the message to the handler
responsible for that type. The handler should respond with a message containing the same `id` and
`type`. Its `data` object should contain `{"success": true}` or `"{"error": <some error>}"` on
success or on error.

`rohrpost` natively only provides the `ping` handler, please see Handlers_ below for a guide on
how to write your own handlers.

Usage
-----

Installation
############

From the command line::

    pip install https://github.com/user/repository/archive/branch.zip

Or add this line to your `requirements.txt`::

    https://github.com/user/repository/archive/branch.zip


Routing
#######

Once you have installed `rohrpost` that, you'll need to add the main `rohrpost` handler to your
`routing.py`. You can find details on this in Channels' `routing documentation`_.

.. code:: Python

    from channels import route
    from rohrpost.main import handle_rohrpost_message

    channel_routing = [
        route('websocket.receive', handle_rohrpost_message, path=r'/rohrpost/$'),
    ]

Handlers
########

`rohrpost` provides a set of helper methods for writing your own handlers. Please read the
developer documentation for further information. Most notably, you'll need the `rohrpost_handler`
decorator, and probably at least one of `send_message`, `send_success`, and `send_error`.
This is how the included `ping` handler works:

.. code:: Python

    from rohrpost.message import send_message
    from rohrpost.registry import rohrpost_handler

    @rohrpost_handler('ping')
    def handle_ping(message, request):
        if 'data' in request:
            send_message(
                message=message,
                message_id=request['id'],
                handler='pong',
                data=request['data'],
            )
        else:
            send_message(
                message=message,
                message_id=request['id'],
                handler='pong',
            )


Development
-----------

For development you'll need to have the test environment installed. This is rather large since
`rohrpost` is meant to be used in conjunction with Channels_, Daphne_, Django_ and so on. ::

    pip install -r requirements/dev.txt


Run tests by calling `py.test` in this directory.


.. _ASGI: https://channels.readthedocs.io/en/latest/asgi.html
.. _Channels: https://github.com/django/channels
.. _Daphne: https://github.com/django/daphne/
.. _Django: https://www.djangoproject.com/
.. _rohrpost-js: https://github.com/axsemantics/rohrpost-js
.. _routing documentation: http://channels.readthedocs.io/en/latest/routing.html
