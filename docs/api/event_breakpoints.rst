EventBreakpoints
================

EventBreakpoints permits setting breakpoints on particular operations and
events in targets that run JavaScript but do not have a DOM.
JavaScript execution will stop on these operations as if there was a regular
breakpoint set.

*This CDP domain is experimental.*

.. module:: cdp.event_breakpoints

* Types_
* Commands_
* Events_

Types
-----

*There are no types in this module.*

Commands
--------

Each command is a generator function. The return
type ``Generator[x, y, z]`` indicates that the generator
*yields* arguments of type ``x``, it must be resumed with
an argument of type ``y``, and it returns type ``z``. In
this library, types ``x`` and ``y`` are the same for all
commands, and ``z`` is the return type you should pay attention
to. For more information, see
:ref:`Getting Started: Commands <getting-started-commands>`.

.. autofunction:: remove_instrumentation_breakpoint

.. autofunction:: set_instrumentation_breakpoint

Events
------

*There are no events in this module.*
