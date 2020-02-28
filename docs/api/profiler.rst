Profiler
========

.. module:: cdp.profiler

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: ProfileNode
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Profile
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: PositionTickInfo
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CoverageRange
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: FunctionCoverage
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ScriptCoverage
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TypeObject
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TypeProfileEntry
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ScriptTypeProfile
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: get_best_effort_coverage

.. autofunction:: set_sampling_interval

.. autofunction:: start

.. autofunction:: start_precise_coverage

.. autofunction:: start_type_profile

.. autofunction:: stop

.. autofunction:: stop_precise_coverage

.. autofunction:: stop_type_profile

.. autofunction:: take_precise_coverage

.. autofunction:: take_type_profile

Events
------

.. autoclass:: ConsoleProfileFinished
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ConsoleProfileStarted
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
