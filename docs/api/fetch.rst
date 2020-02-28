Fetch
=====

A domain for letting clients substitute browser's network layer with client code.

*This CDP domain is experimental.*

.. module:: cdp.fetch

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: RequestId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: RequestStage
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: RequestPattern
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: HeaderEntry
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AuthChallenge
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AuthChallengeResponse
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: continue_request

.. autofunction:: continue_with_auth

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: fail_request

.. autofunction:: fulfill_request

.. autofunction:: get_response_body

.. autofunction:: take_response_body_as_stream

Events
------

.. autoclass:: RequestPaused
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AuthRequired
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
