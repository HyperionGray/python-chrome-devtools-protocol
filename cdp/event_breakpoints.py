# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: EventBreakpoints (experimental)

from __future__ import annotations
from cdp.util import event_class, T_JSON_DICT
from dataclasses import dataclass
import enum
import typing


def set_instrumentation_breakpoint(
        event_name: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Sets breakpoint on particular native event.

    :param event_name: Instrumentation name to stop on.
    '''
    params: T_JSON_DICT = dict()
    params['eventName'] = event_name
    cmd_dict: T_JSON_DICT = {
        'method': 'EventBreakpoints.setInstrumentationBreakpoint',
        'params': params,
    }
    json = yield cmd_dict


def remove_instrumentation_breakpoint(
        event_name: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Removes breakpoint on particular native event.

    :param event_name: Instrumentation name to stop on.
    '''
    params: T_JSON_DICT = dict()
    params['eventName'] = event_name
    cmd_dict: T_JSON_DICT = {
        'method': 'EventBreakpoints.removeInstrumentationBreakpoint',
        'params': params,
    }
    json = yield cmd_dict
