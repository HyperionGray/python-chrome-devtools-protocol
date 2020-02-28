Memory
======

*This CDP domain is experimental.*

.. module:: cdp.memory

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: PressureLevel
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SamplingProfileNode
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SamplingProfile
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Module
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: forcibly_purge_java_script_memory

.. autofunction:: get_all_time_sampling_profile

.. autofunction:: get_browser_sampling_profile

.. autofunction:: get_dom_counters

.. autofunction:: get_sampling_profile

.. autofunction:: prepare_for_leak_detection

.. autofunction:: set_pressure_notifications_suppressed

.. autofunction:: simulate_pressure_notification

.. autofunction:: start_sampling

.. autofunction:: stop_sampling

Events
------
