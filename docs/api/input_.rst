Input
=====

.. module:: cdp.input_

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: TouchPoint
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: GestureSourceType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TimeSinceEpoch
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: dispatch_key_event

.. autofunction:: dispatch_mouse_event

.. autofunction:: dispatch_touch_event

.. autofunction:: emulate_touch_from_mouse_event

.. autofunction:: insert_text

.. autofunction:: set_ignore_input_events

.. autofunction:: synthesize_pinch_gesture

.. autofunction:: synthesize_scroll_gesture

.. autofunction:: synthesize_tap_gesture

Events
------
