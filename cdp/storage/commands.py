'''
DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.

Domain: storage
Experimental: True
'''

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from .types import *


def clear_data_for_origin(
        origin: str,
        storage_types: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Clears storage for origin.
    
    :param origin: Security origin.
    :param storage_types: Comma separated list of StorageType to clear.
    '''
    params: T_JSON_DICT = {
        'origin': origin,
        'storageTypes': storage_types,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Storage.clearDataForOrigin',
        'params': params,
    }
    json = yield cmd_dict


def get_usage_and_quota(
        origin: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,dict]:
    '''
    Returns usage and quota in bytes.
    
    :param origin: Security origin.
    :returns: a dict with the following keys:
        * usage: Storage usage (bytes).
        * quota: Storage quota (bytes).
        * usageBreakdown: Storage usage per type (bytes).
    '''
    params: T_JSON_DICT = {
        'origin': origin,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Storage.getUsageAndQuota',
        'params': params,
    }
    json = yield cmd_dict
    result: T_JSON_DICT = {
        'usage': float(json['usage']),
        'quota': float(json['quota']),
        'usageBreakdown': [UsageForType.from_json(i) for i in json['usageBreakdown']],
    }
    return result


def track_cache_storage_for_origin(
        origin: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Registers origin to be notified when an update occurs to its cache storage list.
    
    :param origin: Security origin.
    '''
    params: T_JSON_DICT = {
        'origin': origin,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Storage.trackCacheStorageForOrigin',
        'params': params,
    }
    json = yield cmd_dict


def track_indexed_db_for_origin(
        origin: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Registers origin to be notified when an update occurs to its IndexedDB.
    
    :param origin: Security origin.
    '''
    params: T_JSON_DICT = {
        'origin': origin,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Storage.trackIndexedDBForOrigin',
        'params': params,
    }
    json = yield cmd_dict


def untrack_cache_storage_for_origin(
        origin: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Unregisters origin from receiving notifications for cache storage.
    
    :param origin: Security origin.
    '''
    params: T_JSON_DICT = {
        'origin': origin,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Storage.untrackCacheStorageForOrigin',
        'params': params,
    }
    json = yield cmd_dict


def untrack_indexed_db_for_origin(
        origin: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Unregisters origin from receiving notifications for IndexedDB.
    
    :param origin: Security origin.
    '''
    params: T_JSON_DICT = {
        'origin': origin,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Storage.untrackIndexedDBForOrigin',
        'params': params,
    }
    json = yield cmd_dict


