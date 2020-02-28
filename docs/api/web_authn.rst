WebAuthn
========

This domain allows configuring virtual authenticators to test the WebAuthn
API.

*This CDP domain is experimental.*

.. module:: cdp.web_authn

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: AuthenticatorId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AuthenticatorProtocol
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AuthenticatorTransport
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: VirtualAuthenticatorOptions
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Credential
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: add_credential

.. autofunction:: add_virtual_authenticator

.. autofunction:: clear_credentials

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: get_credentials

.. autofunction:: remove_virtual_authenticator

.. autofunction:: set_user_verified

Events
------
