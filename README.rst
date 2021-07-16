rohrpost |ghactions| |coveralls| |pypi|
=======================================

`rohrpost` is a simple WebSocket protocol that works well with Django_ using
Channels_. It will interface with every service implementing the ASGI_
specification (which, at the moment, is primarily Channels_ with Daphne_).

The client implementation is rohrpost-js_.

Capabilities
------------

`rohrpost` specifies a very simple protocol with messages looking like this:

.. code:: JSON

    {
        "id": 123,
        "type": "ping",
        "data": "something",
    }

This message will be handled by the ping handler (which rohrpost provides out
of the box). You can add custom handlers using a method decorator. Please see
`our documentation`_ for details on the protocol and handler implementation.

`rohrpost` also provides a mixin for Django_ models to push notifications on
changes (create, update, delete).

Installation
------------

From the command line::

    pip install rohrpost

Or add this line to your `requirements.txt`::

    rohrpost==3.*

Development
-----------

For development you'll need to have the test environment installed. This is
rather large since `rohrpost` works mainly in conjunction with Channels_,
Daphne_, Django_ and so on. ::

    pip install -r requirements/dev.txt

Run tests and style checks in this directory::

    python -m pytest
    python -m isort .
    python -m black rohrpost tests
    python -m flake8
    python -m pytest --pylint --pylint-rcfile=$(pwd)/pyproject.toml --pylint-jobs=0


.. _ASGI: https://channels.readthedocs.io/en/latest/asgi.html
.. _Channels: https://github.com/django/channels
.. _Daphne: https://github.com/django/daphne/
.. _Django: https://www.djangoproject.com/
.. _rohrpost-js: https://github.com/axsemantics/rohrpost-js
.. _our documentation: https://rohrpost.readthedocs.io
.. |ghactions| image:: https://github.com/axsemantics/rohrpost/workflows/Tests/badge.svg
    :target: https://github.com/axsemantics/rohrpost/actions/workflows/tests.yml
.. |coveralls| image:: https://coveralls.io/repos/github/axsemantics/rohrpost/badge.svg?branch=main
    :target: https://coveralls.io/github/axsemantics/rohrpost?branch=main
.. |pypi| image:: https://img.shields.io/pypi/v/rohrpost.svg
    :target: https://pypi.python.org/pypi/rohrpost/
