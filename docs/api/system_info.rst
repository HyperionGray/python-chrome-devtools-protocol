SystemInfo
==========

The SystemInfo domain defines methods and events for querying low-level system information.

*This CDP domain is experimental.*

.. module:: cdp.system_info

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: GPUDevice
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Size
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: VideoDecodeAcceleratorCapability
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: VideoEncodeAcceleratorCapability
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SubsamplingFormat
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ImageDecodeAcceleratorCapability
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: GPUInfo
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ProcessInfo
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: get_info

.. autofunction:: get_process_info

Events
------
