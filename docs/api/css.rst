CSS
===

This domain exposes CSS read/write operations. All CSS objects (stylesheets, rules, and styles)
have an associated `id` used in subsequent operations on the related object. Each object type has
a specific `id` structure, and those are not interchangeable between objects of different kinds.
CSS objects can be loaded using the `get*ForNode()` calls (which accept a DOM node id). A client
can also keep track of stylesheets via the `styleSheetAdded`/`styleSheetRemoved` events and
subsequently load the required stylesheet contents using the `getStyleSheet[Text]()` methods.

*This CDP domain is experimental.*

.. module:: cdp.css

* Types_
* Commands_
* Events_

Types
-----

Generally, you do not need to instantiate CDP types
yourself. Instead, the API creates objects for you as return
values from commands, and then you can use those objects as
arguments to other commands.

.. autoclass:: StyleSheetId
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: StyleSheetOrigin
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: PseudoElementMatches
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: InheritedStyleEntry
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: RuleMatch
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: Value
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SelectorList
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CSSStyleSheetHeader
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CSSRule
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: RuleUsage
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: SourceRange
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: ShorthandEntry
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CSSComputedStyleProperty
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CSSStyle
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CSSProperty
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CSSMedia
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: MediaQuery
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: MediaQueryExpression
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CSSContainerQuery
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: PlatformFontUsage
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: FontVariationAxis
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: FontFace
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CSSKeyframesRule
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: CSSKeyframeRule
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: StyleDeclarationEdit
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

.. autofunction:: add_rule

.. autofunction:: collect_class_names

.. autofunction:: create_style_sheet

.. autofunction:: disable

.. autofunction:: enable

.. autofunction:: force_pseudo_state

.. autofunction:: get_background_colors

.. autofunction:: get_computed_style_for_node

.. autofunction:: get_inline_styles_for_node

.. autofunction:: get_matched_styles_for_node

.. autofunction:: get_media_queries

.. autofunction:: get_platform_fonts_for_node

.. autofunction:: get_style_sheet_text

.. autofunction:: set_container_query_text

.. autofunction:: set_effective_property_value_for_node

.. autofunction:: set_keyframe_key

.. autofunction:: set_local_fonts_enabled

.. autofunction:: set_media_text

.. autofunction:: set_rule_selector

.. autofunction:: set_style_sheet_text

.. autofunction:: set_style_texts

.. autofunction:: start_rule_usage_tracking

.. autofunction:: stop_rule_usage_tracking

.. autofunction:: take_computed_style_updates

.. autofunction:: take_coverage_delta

.. autofunction:: track_computed_style_updates

Events
------

Generally, you do not need to instantiate CDP events
yourself. Instead, the API creates events for you and then
you use the event's attributes.

.. autoclass:: FontsUpdated
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: MediaQueryResultChanged
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: StyleSheetAdded
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: StyleSheetChanged
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json

.. autoclass:: StyleSheetRemoved
      :members:
      :undoc-members:
      :exclude-members: from_json, to_json
