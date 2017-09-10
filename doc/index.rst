rohrpost – a protocol for Django Channels
=========================================

Welcome to the rohrpost documentation!

rohrpost is a small library that aims to make protocol development for `Django's`_
sub-project channels_ (which provides WebSockets capabilities) easy and fun.

It features a light weight, JSON based protocol, including an exemplary handler
implementing a ping/pong method. It also comes with a variety of helper methods,
and Django model mixins that allow to automatically send updates when an object
is updated, deleted, or created.

Protocol
--------

The rohrpost protocol sits on top of channels_ inside the ``text`` component
of a channels message. rohrpost expects this ``text`` component to be valid
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

Using the mixins
----------------

There are four relevant Django model mixins in ``rohrpost.mixins``:
``NotifyOnCreate``, ``NotifyOnUpdate``, ``NotifyOnDelete`` and
``NotifyOnChange`` which inherits from the previous three classes.

On all of these classes, you'll need to set some fields or implement
some methods:

- ``get_group_name(self, message_type)`` or ``group_name``, with the method
  having preference over the attribute. This method or attribute should return
  a string that denotes the group receiving the message. All users in that
  group will receive a message. This gives you the possibility to build
  per-object, per-class or global groups.
  If neither the message nor the attribute are given, the group name is
  the lower cased class name combined with the object's ID:
  f'{object.__class__.__name__.lower()}-{object.pk}'
- ``get_push_notification_data(self, updated_fields, message_type)`` returning a dictionary
  (or any data structure) containing the data you wish to send to the client.
  The serialized object will be updated with an ``updated_fields`` attribute with a list *if*
  ``updated_fields`` was not set by the ``get_push_notification_data()``
  *and* if it was set when calling the ``save()`` method.
  The fallback value if the method is not implemented is ``{"id": obj.id}``.

The message will look like this::

    {
        "id": <some id>,
        "type": "subscription-update",
        "data": {
            "type": <create|update|delete>,
            "group": <group-name>,
            "object": <serialized object>,
        }
    }


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

.. toctree::
   :maxdepth: 1
   :caption: Contents:

.. _channels: https://github.com/django/channels
.. _Django's: http://djangoproject.com/
