Log
===

Provides access to log entries.

.. module:: cdp.log

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: LogEntry
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ViolationSetting
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: clear

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: start_violations_report

.. autofunction:: stop_violations_report

Events
------

.. autoclass:: EntryAdded
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
