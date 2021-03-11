Changelog
=========

unreleased
----------

- **Breaking:** The minimal required Python release is 3.6.
- **Breaking:** rohrpost has now an explicit dependency on Channels >= 3.
- Make support for Python 3.9 official.

2.0.1
-----

- Make support for Python 3.8 official.

2.0.0
-----

- **Breaking:** Utility functions no longer accept ``**additional_data``
- **Breaking:** Utility functions that previously required a kwargs ``message``
  require now a kwarg ``consumer`` which should be an instance of
  ``channels.generic.websocket.WebsocketConsumer``.  The type is not enforced.
- **Breaking:** The utility functions no longer accept ``close`` as an argument.
  This was previously introduced due to Channel 1's interface.  Since closing a
  connection with Channels 2 is a simple call to ``consumer.close()`` and
  because this feature was used only in a small amout of actual calls, this has
  been removed. The caller of the utility functions needs a reference to the
  ``consumer`` anyway and can therefore easily close the connection itself.
- **Breaking:** The minimal required Python release is 3.5.
- **Breaking:** rohrpost has now an explicit dependency on Channels >= 2.
  Since we do not know of any alternatives, we removed this possible
  abstraction.  Feel free to open an issue if this is a problem.
- A ``rohrpost.sync_consumer.SyncRohrpostConsumer`` was added.  It includes
  convenience methods to add/remove a client to/from a group.

1.1.0
-----

- Deprecate ``**additional_data`` in utility functions

1.0.1
-----

- Add long description to project page at pypi.org
