Emulation
=========

This domain emulates different environments for the page.

.. module:: cdp.emulation

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: ScreenOrientation
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: VirtualTimePolicy
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: can_emulate

.. autofunction:: clear_device_metrics_override

.. autofunction:: clear_geolocation_override

.. autofunction:: reset_page_scale_factor

.. autofunction:: set_cpu_throttling_rate

.. autofunction:: set_default_background_color_override

.. autofunction:: set_device_metrics_override

.. autofunction:: set_document_cookie_disabled

.. autofunction:: set_emit_touch_events_for_mouse

.. autofunction:: set_emulated_media

.. autofunction:: set_focus_emulation_enabled

.. autofunction:: set_geolocation_override

.. autofunction:: set_navigator_overrides

.. autofunction:: set_page_scale_factor

.. autofunction:: set_script_execution_disabled

.. autofunction:: set_scrollbars_hidden

.. autofunction:: set_timezone_override

.. autofunction:: set_touch_emulation_enabled

.. autofunction:: set_user_agent_override

.. autofunction:: set_virtual_time_policy

.. autofunction:: set_visible_size

Events
------

.. autoclass:: VirtualTimeBudgetExpired
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
