Inspector
=========

*This CDP domain is experimental.*

.. module:: cdp.inspector

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

Commands
--------

.. autofunction:: disable

.. autofunction:: enable

Events
------

.. autoclass:: Detached
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TargetCrashed
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TargetReloadedAfterCrash
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
