LayerTree
=========

*This CDP domain is experimental.*

.. module:: cdp.layer_tree

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: LayerId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SnapshotId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ScrollRect
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: StickyPositionConstraint
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: PictureTile
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Layer
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: PaintProfile
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: compositing_reasons

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: load_snapshot

.. autofunction:: make_snapshot

.. autofunction:: profile_snapshot

.. autofunction:: release_snapshot

.. autofunction:: replay_snapshot

.. autofunction:: snapshot_command_log

Events
------

.. autoclass:: LayerPainted
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: LayerTreeDidChange
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
