rohrpost – a protocol for Django Channels
=========================================

Welcome to the rohrpost documentation!

rohrpost is a small library that aims to make protocol development for `Django's`_
sub-project channels_ (which provides websockets capabilities) easy and fun.

It features a light weight, JSON based protocol, inculding an exemplary handler
implementing a ping/pong method. It also comes with a variety of helper methods,
and Django model mixins that allow to automatically send updates when an object
is updated, deleted, or created.

Protocol
--------

The rohrpost protocol sits on top of channels_ inside the ``text`` component
of a channels message. Rohrpost expects this ``text`` component to be valid
JSON with

- An ``id`` field that will be sent back in the response.
- A ``type`` field that contains a string defining the message type
  (and hence, which handler will process the message).
- An optional ``data`` field containing whatever should be transmitted
  to the handler. Please note that all request data will be given to the
  handler, and the naming of the ``data`` field is convention only.

A typical message would look like this:

.. code-block:: JSON

   {
       "id": 1234,
       "handler": "ping",
       "data": [1, 2, 3, 4]
   }

Adding Handlers
---------------

rohrpost provides a decorator ``rohrpost_handler``, that accepts both a string
and a list to register a method as the handler for incoming messages.
This is how the ping method is implemented:

.. code-block:: python

   from rohrpost.message import send_message
   from rohrpost.registry import rohrpost_handler


   @rohrpost_handler('ping')
   def handle_ping(message, request):
    response_kwargs = {
        'message': message,
        'message_id': request['id'],
        'handler': 'pong'
    }
    if 'data' in request:
        response_kwargs['data'] = request['data']
    send_message(**response_kwargs)
Utility methods
---------------

rohrpost provides three main helper methods for message sending in ``rohrpost.message``:

- ``rohrpost.message.send_message``
  - ``message``: The original message you are replying to (**required**).
  - ``handler``: The string identifying your handler (**required**).
  - ``message_id``: The message ID (any simple datatype allowed). If none is provided, an integer will be randomly chosen.
  - ``close``: Set to ``True`` if you want to close the connection.
  - ``error``: Include an error message or error content
  - ``**additional_data``: Any other keyword argument will be included in the message in the ``data`` field as a JSON object.
- ``rohrpost.message.send_error`` sends an error message explicitly, takes the same arguments as ``send_message``.
