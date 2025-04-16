Audits
======

Audits domain allows investigation of page violations and possible improvements.

*This CDP domain is experimental.*

.. module:: cdp.audits

* Types_
* Commands_
* Events_

Types
-----

Generally, you do not need to instantiate CDP types
yourself. Instead, the API creates objects for you as return
values from commands, and then you can use those objects as
arguments to other commands.

.. autoclass:: AffectedCookie
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AffectedRequest
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AffectedFrame
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SameSiteCookieExclusionReason
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SameSiteCookieWarningReason
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SameSiteCookieOperation
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SameSiteCookieIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: MixedContentResolutionStatus
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: MixedContentResourceType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: MixedContentIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: BlockedByResponseReason
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: BlockedByResponseIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: HeavyAdResolutionStatus
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: HeavyAdReason
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: HeavyAdIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ContentSecurityPolicyViolationType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SourceCodeLocation
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ContentSecurityPolicyIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SharedArrayBufferIssueType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SharedArrayBufferIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TwaQualityEnforcementViolationType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: TrustedWebActivityIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: LowTextContrastIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CorsIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AttributionReportingIssueType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: AttributionReportingIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: QuirksModeIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: NavigatorUserAgentIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: WasmCrossOriginModuleSharingIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: GenericIssueErrorType
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: GenericIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: DeprecationIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ClientHintIssueReason
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ClientHintIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: InspectorIssueCode
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: InspectorIssueDetails
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: IssueId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: InspectorIssue
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

.. autofunction:: check_contrast

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: get_encoded_response

Events
------

Generally, you do not need to instantiate CDP events
yourself. Instead, the API creates events for you and then
you use the event's attributes.

.. autoclass:: IssueAdded
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
