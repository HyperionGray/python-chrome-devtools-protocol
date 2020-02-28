Cast
====

A domain for interacting with Cast, Presentation API, and Remote Playback API
functionalities.

*This CDP domain is experimental.*

.. module:: cdp.cast

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: Sink
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: set_sink_to_use

.. autofunction:: start_tab_mirroring

.. autofunction:: stop_casting

Events
------

.. autoclass:: SinksUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: IssueUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
