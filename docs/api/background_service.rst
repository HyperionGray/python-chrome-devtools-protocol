BackgroundService
=================

Defines events for background web platform features.

*This CDP domain is experimental.*

.. module:: cdp.background_service

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: ServiceName
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: EventMetadata
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: BackgroundServiceEvent
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: clear_events

.. autofunction:: set_recording

.. autofunction:: start_observing

.. autofunction:: stop_observing

Events
------

.. autoclass:: RecordingStateChanged
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: BackgroundServiceEventReceived
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
