Console
=======

This domain is deprecated - use Runtime or Log instead.

.. module:: cdp.console

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: ConsoleMessage
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: clear_messages

.. autofunction:: disable

.. autofunction:: enable

Events
------

.. autoclass:: MessageAdded
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
