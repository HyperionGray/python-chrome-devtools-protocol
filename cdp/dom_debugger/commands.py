'''
DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.

Domain: dom_debugger
Experimental: False
'''

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from .types import *
from ..dom import types as dom
from ..runtime import types as runtime



def get_event_listeners(
        object_id: runtime.RemoteObjectId,
        depth: typing.Optional[int] = None,
        pierce: typing.Optional[bool] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List['EventListener']]:
    '''
    Returns event listeners of the given object.
    
    :param object_id: Identifier of the object to return listeners for.
    :param depth: The maximum depth at which Node children should be retrieved, defaults to 1. Use -1 for the
    entire subtree or provide an integer larger than 0.
    :param pierce: Whether or not iframes and shadow roots should be traversed when returning the subtree
    (default is false). Reports listeners for all contexts if pierce is enabled.
    :returns: Array of relevant listeners.
    '''
    params: T_JSON_DICT = {
        'objectId': object_id.to_json(),
    }
    if depth is not None:
        params['depth'] = depth
    if pierce is not None:
        params['pierce'] = pierce
    cmd_dict: T_JSON_DICT = {
        'method': 'DOMDebugger.getEventListeners',
        'params': params,
    }
    json = yield cmd_dict
    return [EventListener.from_json(i) for i in json['listeners']]


def remove_dom_breakpoint(
        node_id: dom.NodeId,
        type: DOMBreakpointType,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Removes DOM breakpoint that was set using `setDOMBreakpoint`.
    
    :param node_id: Identifier of the node to remove breakpoint from.
    :param type: Type of the breakpoint to remove.
    '''
    params: T_JSON_DICT = {
        'nodeId': node_id.to_json(),
        'type': type.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'DOMDebugger.removeDOMBreakpoint',
        'params': params,
    }
    json = yield cmd_dict


def remove_event_listener_breakpoint(
        event_name: str,
        target_name: typing.Optional[str] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Removes breakpoint on particular DOM event.
    
    :param event_name: Event name.
    :param target_name: EventTarget interface name.
    '''
    params: T_JSON_DICT = {
        'eventName': event_name,
    }
    if target_name is not None:
        params['targetName'] = target_name
    cmd_dict: T_JSON_DICT = {
        'method': 'DOMDebugger.removeEventListenerBreakpoint',
        'params': params,
    }
    json = yield cmd_dict


def remove_instrumentation_breakpoint(
        event_name: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Removes breakpoint on particular native event.
    
    :param event_name: Instrumentation name to stop on.
    '''
    params: T_JSON_DICT = {
        'eventName': event_name,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'DOMDebugger.removeInstrumentationBreakpoint',
        'params': params,
    }
    json = yield cmd_dict


def remove_xhr_breakpoint(
        url: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Removes breakpoint from XMLHttpRequest.
    
    :param url: Resource URL substring.
    '''
    params: T_JSON_DICT = {
        'url': url,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'DOMDebugger.removeXHRBreakpoint',
        'params': params,
    }
    json = yield cmd_dict


def set_dom_breakpoint(
        node_id: dom.NodeId,
        type: DOMBreakpointType,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Sets breakpoint on particular operation with DOM.
    
    :param node_id: Identifier of the node to set breakpoint on.
    :param type: Type of the operation to stop upon.
    '''
    params: T_JSON_DICT = {
        'nodeId': node_id.to_json(),
        'type': type.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'DOMDebugger.setDOMBreakpoint',
        'params': params,
    }
    json = yield cmd_dict


def set_event_listener_breakpoint(
        event_name: str,
        target_name: typing.Optional[str] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Sets breakpoint on particular DOM event.
    
    :param event_name: DOM Event name to stop on (any DOM event will do).
    :param target_name: EventTarget interface name to stop on. If equal to `"*"` or not provided, will stop on any
    EventTarget.
    '''
    params: T_JSON_DICT = {
        'eventName': event_name,
    }
    if target_name is not None:
        params['targetName'] = target_name
    cmd_dict: T_JSON_DICT = {
        'method': 'DOMDebugger.setEventListenerBreakpoint',
        'params': params,
    }
    json = yield cmd_dict


def set_instrumentation_breakpoint(
        event_name: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Sets breakpoint on particular native event.
    
    :param event_name: Instrumentation name to stop on.
    '''
    params: T_JSON_DICT = {
        'eventName': event_name,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'DOMDebugger.setInstrumentationBreakpoint',
        'params': params,
    }
    json = yield cmd_dict


def set_xhr_breakpoint(
        url: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Sets breakpoint on XMLHttpRequest.
    
    :param url: Resource URL substring. All XHRs having this substring in the URL will get stopped upon.
    '''
    params: T_JSON_DICT = {
        'url': url,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'DOMDebugger.setXHRBreakpoint',
        'params': params,
    }
    json = yield cmd_dict


