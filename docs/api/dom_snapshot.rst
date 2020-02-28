DOMSnapshot
===========

This domain facilitates obtaining document snapshots with DOM, layout, and style information.

*This CDP domain is experimental.*

.. module:: cdp.dom_snapshot

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: DOMNode
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: InlineTextBox
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: LayoutTreeNode
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ComputedStyle
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: NameValue
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: StringIndex
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ArrayOfStrings
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: RareStringData
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: RareBooleanData
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: RareIntegerData
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Rectangle
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: DocumentSnapshot
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: NodeTreeSnapshot
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: LayoutTreeSnapshot
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TextBoxSnapshot
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: capture_snapshot

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: get_snapshot

Events
------
