ApplicationCache
================

*This CDP domain is experimental.*

.. module:: cdp.application_cache

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: ApplicationCacheResource
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ApplicationCache
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: FrameWithManifest
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: enable

.. autofunction:: get_application_cache_for_frame

.. autofunction:: get_frames_with_manifests

.. autofunction:: get_manifest_for_frame

Events
------

.. autoclass:: ApplicationCacheStatusUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: NetworkStateUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
