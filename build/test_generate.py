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
