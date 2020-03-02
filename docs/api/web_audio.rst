WebAudio
========

This domain allows inspection of Web Audio API.
https://webaudio.github.io/web-audio-api/

*This CDP domain is experimental.*

.. module:: cdp.web_audio

* Types_
* Commands_
* Events_

Types
-----

Generally, you do not need to instantiate CDP types
yourself. Instead, the API creates objects for you as return
values from commands, and then you can use those objects as
arguments to other commands.

.. autoclass:: ContextId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ContextType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ContextState
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ContextRealtimeData
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: BaseAudioContext
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

.. autofunction:: get_realtime_data

Events
------

Generally, you do not need to instantiate CDP events
yourself. Instead, the API creates events for you and then
you use the event's attributes.

.. autoclass:: ContextCreated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ContextDestroyed
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ContextChanged
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
