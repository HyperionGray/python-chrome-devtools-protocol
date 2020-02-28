Animation
=========

*This CDP domain is experimental.*

.. module:: cdp.animation

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: Animation
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AnimationEffect
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: KeyframesRule
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: KeyframeStyle
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: get_current_time

.. autofunction:: get_playback_rate

.. autofunction:: release_animations

.. autofunction:: resolve_animation

.. autofunction:: seek_animations

.. autofunction:: set_paused

.. autofunction:: set_playback_rate

.. autofunction:: set_timing

Events
------

.. autoclass:: AnimationCanceled
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AnimationCreated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AnimationStarted
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
