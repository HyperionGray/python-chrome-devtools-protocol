Security
========

Security

.. module:: cdp.security

* Types_
* Commands_
* Events_

Types
-----

Generally you do not need to instantiate CDP types yourself. Instead, the API creates objects for you as return values from commands, and then you can use those objects as arguments to other commands.

.. autoclass:: CertificateId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: MixedContentType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SecurityState
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SecurityStateExplanation
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: InsecureContentStatus
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CertificateErrorAction
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

Commands
--------

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: handle_certificate_error

.. autofunction:: set_ignore_certificate_errors

.. autofunction:: set_override_certificate_errors

Events
------

.. autoclass:: CertificateError
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SecurityStateChanged
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
