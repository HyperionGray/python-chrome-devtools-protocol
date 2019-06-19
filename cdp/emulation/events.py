'''
DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.

Domain: emulation
Experimental: False
'''

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from .types import *


@dataclass
class VirtualTimeBudgetExpired:
    '''
    Notification sent after the virtual time budget for the current VirtualTimePolicy has run out.
    '''
    # These fields are used for internal purposes and are not part of CDP
    _domain = 'Emulation'
    _method = 'virtualTimeBudgetExpired'

    @classmethod
    def from_json(cls, json: dict) -> 'VirtualTimeBudgetExpired':
        return cls(
        )

