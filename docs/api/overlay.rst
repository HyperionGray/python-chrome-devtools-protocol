Overlay
=======

This domain provides various functionality related to drawing atop the inspected page.

*This CDP domain is experimental.*

.. module:: cdp.overlay

* Types_
* Commands_
* Events_

Types
-----

Generally, you do not need to instantiate CDP types
yourself. Instead, the API creates objects for you as return
values from commands, and then you can use those objects as
arguments to other commands.

.. autoclass:: HighlightConfig
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: InspectMode
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

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

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: get_highlight_object_for_test

.. autofunction:: hide_highlight

.. autofunction:: highlight_frame

.. autofunction:: highlight_node

.. autofunction:: highlight_quad

.. autofunction:: highlight_rect

.. autofunction:: set_inspect_mode

.. autofunction:: set_paused_in_debugger_message

.. autofunction:: set_show_ad_highlights

.. autofunction:: set_show_debug_borders

.. autofunction:: set_show_fps_counter

.. autofunction:: set_show_hit_test_borders

.. autofunction:: set_show_layout_shift_regions

.. autofunction:: set_show_paint_rects

.. autofunction:: set_show_scroll_bottleneck_rects

.. autofunction:: set_show_viewport_size_on_resize

Events
------

Generally, you do not need to instantiate CDP events
yourself. Instead, the API creates events for you and then
you use the event's attributes.

.. autoclass:: InspectNodeRequested
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: NodeHighlightRequested
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ScreenshotRequested
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: InspectModeCanceled
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
