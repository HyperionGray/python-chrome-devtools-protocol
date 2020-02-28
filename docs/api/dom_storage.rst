DOMStorage
==========

Query and modify DOM storage.

*This CDP domain is experimental.*

.. module:: cdp.dom_storage

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: StorageId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Item
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: clear

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: get_dom_storage_items

.. autofunction:: remove_dom_storage_item

.. autofunction:: set_dom_storage_item

Events
------

.. autoclass:: DomStorageItemAdded
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: DomStorageItemRemoved
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: DomStorageItemUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: DomStorageItemsCleared
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
