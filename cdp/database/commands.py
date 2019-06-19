'''
DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.

Domain: database
Experimental: True
'''

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from .types import *


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Disables database tracking, prevents database events from being sent to the client.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Database.disable',
    }
    json = yield cmd_dict


def enable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enables database tracking, database events will now be delivered to the client.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Database.enable',
    }
    json = yield cmd_dict


def execute_sql(
        database_id: DatabaseId,
        query: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,dict]:
    '''
    
    
    :param database_id: 
    :param query: 
    :returns: a dict with the following keys:
        * columnNames: (Optional) 
        * values: (Optional) 
        * sqlError: (Optional) 
    '''
    params: T_JSON_DICT = {
        'databaseId': database_id.to_json(),
        'query': query,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Database.executeSQL',
        'params': params,
    }
    json = yield cmd_dict
    result: T_JSON_DICT = {
    }
    if 'columnNames' in json:
        result['columnNames'] = [str(i) for i in json['columnNames']]
    if 'values' in json:
        result['values'] = [i for i in json['values']]
    if 'sqlError' in json:
        result['sqlError'] = Error.from_json(json['sqlError'])
    return result


def get_database_table_names(
        database_id: DatabaseId,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List['str']]:
    '''
    
    
    :param database_id: 
    :returns: 
    '''
    params: T_JSON_DICT = {
        'databaseId': database_id.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Database.getDatabaseTableNames',
        'params': params,
    }
    json = yield cmd_dict
    return [str(i) for i in json['tableNames']]


