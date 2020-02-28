Storage
=======

*This CDP domain is experimental.*

.. module:: cdp.storage

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: StorageType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: UsageForType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: clear_data_for_origin

.. autofunction:: get_usage_and_quota

.. autofunction:: track_cache_storage_for_origin

.. autofunction:: track_indexed_db_for_origin

.. autofunction:: untrack_cache_storage_for_origin

.. autofunction:: untrack_indexed_db_for_origin

Events
------

.. autoclass:: CacheStorageContentUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CacheStorageListUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: IndexedDBContentUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: IndexedDBListUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
