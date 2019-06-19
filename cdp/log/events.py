'''
DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.

Domain: log
Experimental: False
'''

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from .types import *


@dataclass
class EntryAdded:
    '''
    Issued when new message was logged.
    '''
    #: Issued when new message was logged.
    entry: LogEntry

    # These fields are used for internal purposes and are not part of CDP
    _domain = 'Log'
    _method = 'entryAdded'

    @classmethod
    def from_json(cls, json: dict) -> 'EntryAdded':
        return cls(
            entry=LogEntry.from_json(json['entry']),
        )

