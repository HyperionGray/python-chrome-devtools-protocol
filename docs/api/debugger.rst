Debugger
========

Debugger domain exposes JavaScript debugging capabilities. It allows setting and removing
breakpoints, stepping through execution, exploring stack traces, etc.

.. module:: cdp.debugger

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: BreakpointId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CallFrameId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Location
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ScriptPosition
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CallFrame
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Scope
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SearchMatch
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: BreakLocation
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: continue_to_location

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: evaluate_on_call_frame

.. autofunction:: get_possible_breakpoints

.. autofunction:: get_script_source

.. autofunction:: get_stack_trace

.. autofunction:: pause

.. autofunction:: pause_on_async_call

.. autofunction:: remove_breakpoint

.. autofunction:: restart_frame

.. autofunction:: resume

.. autofunction:: search_in_content

.. autofunction:: set_async_call_stack_depth

.. autofunction:: set_blackbox_patterns

.. autofunction:: set_blackboxed_ranges

.. autofunction:: set_breakpoint

.. autofunction:: set_breakpoint_by_url

.. autofunction:: set_breakpoint_on_function_call

.. autofunction:: set_breakpoints_active

.. autofunction:: set_instrumentation_breakpoint

.. autofunction:: set_pause_on_exceptions

.. autofunction:: set_return_value

.. autofunction:: set_script_source

.. autofunction:: set_skip_all_pauses

.. autofunction:: set_variable_value

.. autofunction:: step_into

.. autofunction:: step_out

.. autofunction:: step_over

Events
------

.. autoclass:: BreakpointResolved
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Paused
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Resumed
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ScriptFailedToParse
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ScriptParsed
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
