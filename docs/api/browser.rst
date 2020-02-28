Browser
=======

The Browser domain defines methods and events for browser managing.

.. module:: cdp.browser

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: WindowID
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: WindowState
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Bounds
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: PermissionType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Bucket
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Histogram
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: close

.. autofunction:: crash

.. autofunction:: crash_gpu_process

.. autofunction:: get_browser_command_line

.. autofunction:: get_histogram

.. autofunction:: get_histograms

.. autofunction:: get_version

.. autofunction:: get_window_bounds

.. autofunction:: get_window_for_target

.. autofunction:: grant_permissions

.. autofunction:: reset_permissions

.. autofunction:: set_dock_tile

.. autofunction:: set_window_bounds

Events
------
