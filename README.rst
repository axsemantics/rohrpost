rohrpost
========

**`rohrpost` is still very much a WIP project. Its interface and structure may still be subject
to unpredictable changes.**

`rohrpost` is a simple WebSocket protocol. It is designed to work with Django_ using Channels_ but
will interface with every base service implementing the ASGI_ specification (which, at the moment,
is mostly Channels_ with Daphne_).

The client implementation is rohrpost-js_.


.. _ASGI: https://channels.readthedocs.io/en/latest/asgi.html
.. _Channels: https://github.com/django/channels
.. _Daphne: https://github.com/django/daphne/
.. _Django: https://www.djangoproject.com/
.. _rohrpost-js: https://github.com/axsemantics/rohrpost-js
