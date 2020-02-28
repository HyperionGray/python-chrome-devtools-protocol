Database
========

*This CDP domain is experimental.*

.. module:: cdp.database

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: DatabaseId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Database
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Error
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: execute_sql

.. autofunction:: get_database_table_names

Events
------

.. autoclass:: AddDatabase
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
