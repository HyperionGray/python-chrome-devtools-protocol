'''
A combination of unit tests and integration tests.

The main purpose of the tests is to make sure that the CDP spec is converted
into Python code correctly, i.e. integration testing. But some of the most
complicated logic is also covered by unit tests.

Tests that generate code will typically print the expected and actual values.
Pytest doesn't display stdout by default unless a test fails, and debugging
codegen tests is almost always easier with the values displayed on stdout.
'''

from textwrap import dedent

from generate import CdpType, docstring


def test_docstring():
    description = \
       "Values of AXProperty name:\n- from 'busy' to 'roledescription': " \
       "states which apply to every AX node\n- from 'live' to 'root': " \
       "attributes which apply to nodes in live regions\n- from " \
       "'autocomplete' to 'valuetext': attributes which apply to " \
       "widgets\n- from 'checked' to 'selected': states which apply to " \
       "widgets\n- from 'activedescendant' to 'owns' - relationships " \
       "between elements other than parent/child/sibling."
    expected = dedent("""\
        '''
        Values of AXProperty name:
        - from 'busy' to 'roledescription': states which apply to every AX node
        - from 'live' to 'root': attributes which apply to nodes in live regions
        - from 'autocomplete' to 'valuetext': attributes which apply to widgets
        - from 'checked' to 'selected': states which apply to widgets
        - from 'activedescendant' to 'owns' - relationships between elements other than parent/child/sibling.
        '''""")
    actual = docstring(description)
    print('EXPECTED:', expected)
    print('ACTUAL:', actual)
    assert expected == actual


def test_cdp_primitive_type():
    json_type = {
        "id": "AXNodeId",
        "description": "Unique accessibility node identifier.",
        "type": "string"
    }
    expected = dedent("""\
        class AXNodeId(str):
            '''
            Unique accessibility node identifier.
            '''
            def to_json(self) -> str:
                return self

            @classmethod
            def from_json(cls, json: str) -> 'AXNodeId':
                return cls(json)

            def __repr__(self):
                return 'AXNodeId({})'.format(super().__repr__())""")

    type = CdpType.from_json(json_type)
    actual = type.generate_code()
    print('EXPECTED:', expected)
    print('ACTUAL:', actual)
    assert expected == actual


def test_cdp_enum_type():
    json_type = {
        "id": "AXValueSourceType",
        "description": "Enum of possible property sources.",
        "type": "string",
        "enum": [
            "attribute",
            "implicit",
            "style",
            "contents",
            "placeholder",
            "relatedElement"
        ]
    }
    expected = dedent("""\
        class AXValueSourceType(enum.Enum):
            '''
            Enum of possible property sources.
            '''
            ATTRIBUTE = "attribute"
            IMPLICIT = "implicit"
            STYLE = "style"
            CONTENTS = "contents"
            PLACEHOLDER = "placeholder"
            RELATED_ELEMENT = "relatedElement"

            def to_json(self) -> str:
                return self.value

            @classmethod
            def from_json(cls, json: str) -> 'AXValueSourceType':
                return cls(json)""")

    type = CdpType.from_json(json_type)
    actual = type.generate_code()
    print('EXPECTED:', expected)
    print('ACTUAL:', actual)
    assert expected == actual


def test_cdp_class_type():
    json_type = {
        "id": "AXValue",
        "description": "A single computed AX property.",
        "type": "object",
        "properties": [
            {
                "name": "type",
                "description": "The type of this value.",
                "$ref": "AXValueType"
            },
            {
                "name": "value",
                "description": "The computed value of this property.",
                "optional": True,
                "type": "any"
            },
            {
                "name": "relatedNodes",
                "description": "One or more related nodes, if applicable.",
                "optional": True,
                "type": "array",
                "items": {
                    "$ref": "AXRelatedNode"
                }
            },
            {
                "name": "sources",
                "description": "The sources which contributed to the computation of this property.",
                "optional": True,
                "type": "array",
                "items": {
                    "$ref": "AXValueSource"
                }
            }
        ]
    }
    expected = dedent("""\
        @dataclass
        class AXValue:
            '''
            A single computed AX property.
            '''
            #: The type of this value.
            type: 'AXValueType'

            #: The computed value of this property.
            value: typing.Optional[typing.Any] = None

            #: One or more related nodes, if applicable.
            related_nodes: typing.Optional[typing.List['AXRelatedNode']] = None

            #: The sources which contributed to the computation of this property.
            sources: typing.Optional[typing.List['AXValueSource']] = None

            def to_json(self) -> T_JSON_DICT:
                json: T_JSON_DICT = dict()
                json['type'] = self.type.to_json()
                if self.value is not None:
                    json['value'] = self.value
                if self.related_nodes is not None:
                    json['relatedNodes'] = [i.to_json() for i in self.related_nodes]
                if self.sources is not None:
                    json['sources'] = [i.to_json() for i in self.sources]
                return json

            @classmethod
            def from_json(cls, json: T_JSON_DICT) -> 'AXValue':
                return cls(
                    type=AXValueType.from_json(json['type']),
                    value=json['value'] if 'value' in json else None,
                    relatedNodes=[AXRelatedNode.from_json(i) for i in json['relatedNodes']] if 'relatedNodes' in json else None,
                    sources=[AXValueSource.from_json(i) for i in json['sources']] if 'sources' in json else None,
                )""")

    type = CdpType.from_json(json_type)
    actual = type.generate_code()
    print('EXPECTED:', expected)
    print('ACTUAL:', actual)
    assert expected == actual
