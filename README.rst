
rohrpost |travis| |coveralls| |pypi|
====================================

`rohrpost` is a simple WebSocket protocol. It works well with Django_ using Channels_ but
will interface with every base service implementing the ASGI_ specification (which, at the moment,
is primarily Channels_ with Daphne_).

The client implementation is rohrpost-js_.

Protocol
--------

The `rohrpost` protocol is simple. The client may send messages containing an `id` (integer),
a `type` (string), and an optional data field (any JSON type):

.. code:: JSON

    {
        "id": 123,
        "type": "ping",
        "data": "something",
    }

The server will (if it receives the mandatory fields) try to give the message to the handler
responsible for that type. The handler should respond with a message containing the same `id` and
`type`. Its `data` object should contain {"error": <some error>}"` on errors as a top-level field.
The server may include other related data the data field.

`rohrpost` natively provides the `ping` handler. Please see Handlers_ below for a guide on
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
There is also a `build_message` method that can optionally add a random ID to server-initiated
messages.
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

Mixins
######

`rohrpost` also provides a mixin for Django_ models to push notifications on changes (create,
update, delete). If users should receive these notifications, you have to add them to the
matching group beforehand.

You can find further documentation in `rohrpost/mixin.py`.


Development
-----------

For development you'll need to have the test environment installed. This is rather large since
`rohrpost` works mainly in conjunction with Channels_, Daphne_, Django_ and so on. ::

    pip install -r requirements/dev.txt

Run tests and style checks in this directory::

    py.test
    isort -rc .
    pylama


.. _ASGI: https://channels.readthedocs.io/en/latest/asgi.html
.. _Channels: https://github.com/django/channels
.. _Daphne: https://github.com/django/daphne/
.. _Django: https://www.djangoproject.com/
.. _rohrpost-js: https://github.com/axsemantics/rohrpost-js
.. _routing documentation: http://channels.readthedocs.io/en/latest/routing.html
.. |travis| image:: https://travis-ci.org/axsemantics/rohrpost.svg?branch=master
    :target: https://travis-ci.org/axsemantics/rohrpost
.. |coveralls| image:: https://coveralls.io/repos/github/axsemantics/rohrpost/badge.svg?branch=master
    :target: https://coveralls.io/github/axsemantics/rohrpost?branch=master
.. |pypi| image:: https://img.shields.io/pypi/v/rohrpost.svg
    :target: https://pypi.python.org/pypi/rohrpost/
