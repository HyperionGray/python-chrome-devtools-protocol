'''
DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.

Domain: css
Experimental: True
'''

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from .types import *


@dataclass
class FontsUpdated:
    '''
    Fires whenever a web font is updated.  A non-empty font parameter indicates a successfully loaded
    web font
    '''
    #: Fires whenever a web font is updated.  A non-empty font parameter indicates a successfully loaded
    #: web font
    font: FontFace

    # These fields are used for internal purposes and are not part of CDP
    _domain = 'CSS'
    _method = 'fontsUpdated'

    @classmethod
    def from_json(cls, json: dict) -> 'FontsUpdated':
        return cls(
            font=FontFace.from_json(json['font']),
        )


@dataclass
class MediaQueryResultChanged:
    '''
    Fires whenever a MediaQuery result changes (for example, after a browser window has been
    resized.) The current implementation considers only viewport-dependent media features.
    '''
    # These fields are used for internal purposes and are not part of CDP
    _domain = 'CSS'
    _method = 'mediaQueryResultChanged'

    @classmethod
    def from_json(cls, json: dict) -> 'MediaQueryResultChanged':
        return cls(
        )


@dataclass
class StyleSheetAdded:
    '''
    Fired whenever an active document stylesheet is added.
    '''
    #: Fired whenever an active document stylesheet is added.
    header: CSSStyleSheetHeader

    # These fields are used for internal purposes and are not part of CDP
    _domain = 'CSS'
    _method = 'styleSheetAdded'

    @classmethod
    def from_json(cls, json: dict) -> 'StyleSheetAdded':
        return cls(
            header=CSSStyleSheetHeader.from_json(json['header']),
        )


@dataclass
class StyleSheetChanged:
    '''
    Fired whenever a stylesheet is changed as a result of the client operation.
    '''
    #: Fired whenever a stylesheet is changed as a result of the client operation.
    style_sheet_id: StyleSheetId

    # These fields are used for internal purposes and are not part of CDP
    _domain = 'CSS'
    _method = 'styleSheetChanged'

    @classmethod
    def from_json(cls, json: dict) -> 'StyleSheetChanged':
        return cls(
            style_sheet_id=StyleSheetId.from_json(json['styleSheetId']),
        )


@dataclass
class StyleSheetRemoved:
    '''
    Fired whenever an active document stylesheet is removed.
    '''
    #: Fired whenever an active document stylesheet is removed.
    style_sheet_id: StyleSheetId

    # These fields are used for internal purposes and are not part of CDP
    _domain = 'CSS'
    _method = 'styleSheetRemoved'

    @classmethod
    def from_json(cls, json: dict) -> 'StyleSheetRemoved':
        return cls(
            style_sheet_id=StyleSheetId.from_json(json['styleSheetId']),
        )

