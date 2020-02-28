IO
==

Input/Output operations for streams produced by DevTools.

.. module:: cdp.io

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: StreamHandle
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: close

.. autofunction:: read

.. autofunction:: resolve_blob

Events
------
