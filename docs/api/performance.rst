Performance
===========

.. module:: cdp.performance

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: Metric
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: get_metrics

.. autofunction:: set_time_domain

Events
------

.. autoclass:: Metrics
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
