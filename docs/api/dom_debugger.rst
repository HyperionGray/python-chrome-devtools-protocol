DOMDebugger
===========

DOM debugging allows setting breakpoints on particular DOM operations and events. JavaScript
execution will stop on these operations as if there was a regular breakpoint set.

.. module:: cdp.dom_debugger

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: DOMBreakpointType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: EventListener
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: get_event_listeners

.. autofunction:: remove_dom_breakpoint

.. autofunction:: remove_event_listener_breakpoint

.. autofunction:: remove_instrumentation_breakpoint

.. autofunction:: remove_xhr_breakpoint

.. autofunction:: set_dom_breakpoint

.. autofunction:: set_event_listener_breakpoint

.. autofunction:: set_instrumentation_breakpoint

.. autofunction:: set_xhr_breakpoint

Events
------
