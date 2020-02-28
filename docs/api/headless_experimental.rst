HeadlessExperimental
====================

This domain provides experimental commands only supported in headless mode.

*This CDP domain is experimental.*

.. module:: cdp.headless_experimental

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: ScreenshotParams
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: begin_frame

.. autofunction:: disable

.. autofunction:: enable

Events
------

.. autoclass:: NeedsBeginFramesChanged
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
