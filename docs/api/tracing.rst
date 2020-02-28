Tracing
=======

*This CDP domain is experimental.*

.. module:: cdp.tracing

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: MemoryDumpConfig
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TraceConfig
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: StreamFormat
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: StreamCompression
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: end

.. autofunction:: get_categories

.. autofunction:: record_clock_sync_marker

.. autofunction:: request_memory_dump

.. autofunction:: start

Events
------

.. autoclass:: BufferUsage
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: DataCollected
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TracingComplete
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
