Accessibility
=============

*This CDP domain is experimental.*

.. module:: cdp.accessibility

* Types_
* Commands_
* Events_

Types
-----

Generally, you do not need to instantiate CDP types
yourself. Instead, the API creates objects for you as return
values from commands, and then you can use those objects as
arguments to other commands.

.. autoclass:: AXNodeId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AXValueType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AXValueSourceType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AXValueNativeSourceType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AXValueSource
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AXRelatedNode
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AXProperty
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AXValue
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AXPropertyName
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AXNode
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

.. autofunction:: get_full_ax_tree

.. autofunction:: get_partial_ax_tree

Events
------

*There are no events in this module.*
