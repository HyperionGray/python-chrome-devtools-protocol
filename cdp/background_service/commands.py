'''
DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.

Domain: background_service
Experimental: True
'''

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from .types import *


def start_observing(
        service: ServiceName,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enables event updates for the service.
    
    :param service: 
    '''
    params: T_JSON_DICT = {
        'service': service.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'BackgroundService.startObserving',
        'params': params,
    }
    json = yield cmd_dict


def stop_observing(
        service: ServiceName,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Disables event updates for the service.
    
    :param service: 
    '''
    params: T_JSON_DICT = {
        'service': service.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'BackgroundService.stopObserving',
        'params': params,
    }
    json = yield cmd_dict


def set_recording(
        should_record: bool,
        service: ServiceName,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Set the recording state for the service.
    
    :param should_record: 
    :param service: 
    '''
    params: T_JSON_DICT = {
        'shouldRecord': should_record,
        'service': service.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'BackgroundService.setRecording',
        'params': params,
    }
    json = yield cmd_dict


def clear_events(
        service: ServiceName,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Clears all stored data for the service.
    
    :param service: 
    '''
    params: T_JSON_DICT = {
        'service': service.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'BackgroundService.clearEvents',
        'params': params,
    }
    json = yield cmd_dict


