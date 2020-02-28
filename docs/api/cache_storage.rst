CacheStorage
============

*This CDP domain is experimental.*

.. module:: cdp.cache_storage

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: CacheId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CachedResponseType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: DataEntry
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Cache
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Header
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CachedResponse
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: delete_cache

.. autofunction:: delete_entry

.. autofunction:: request_cache_names

.. autofunction:: request_cached_response

.. autofunction:: request_entries

Events
------
