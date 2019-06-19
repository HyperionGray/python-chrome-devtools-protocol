'''
DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.

Domain: headless_experimental
Experimental: True
'''

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from .types import *


def begin_frame(
        frame_time_ticks: typing.Optional[float] = None,
        interval: typing.Optional[float] = None,
        no_display_updates: typing.Optional[bool] = None,
        screenshot: typing.Optional[ScreenshotParams] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,dict]:
    '''
    Sends a BeginFrame to the target and returns when the frame was completed. Optionally captures a
    screenshot from the resulting frame. Requires that the target was created with enabled
    BeginFrameControl. Designed for use with --run-all-compositor-stages-before-draw, see also
    https://goo.gl/3zHXhB for more background.
    
    :param frame_time_ticks: Timestamp of this BeginFrame in Renderer TimeTicks (milliseconds of uptime). If not set,
    the current time will be used.
    :param interval: The interval between BeginFrames that is reported to the compositor, in milliseconds.
    Defaults to a 60 frames/second interval, i.e. about 16.666 milliseconds.
    :param no_display_updates: Whether updates should not be committed and drawn onto the display. False by default. If
    true, only side effects of the BeginFrame will be run, such as layout and animations, but
    any visual updates may not be visible on the display or in screenshots.
    :param screenshot: If set, a screenshot of the frame will be captured and returned in the response. Otherwise,
    no screenshot will be captured. Note that capturing a screenshot can fail, for example,
    during renderer initialization. In such a case, no screenshot data will be returned.
    :returns: a dict with the following keys:
        * hasDamage: Whether the BeginFrame resulted in damage and, thus, a new frame was committed to the
    display. Reported for diagnostic uses, may be removed in the future.
        * screenshotData: (Optional) Base64-encoded image data of the screenshot, if one was requested and successfully taken.
    '''
    params: T_JSON_DICT = {
    }
    if frame_time_ticks is not None:
        params['frameTimeTicks'] = frame_time_ticks
    if interval is not None:
        params['interval'] = interval
    if no_display_updates is not None:
        params['noDisplayUpdates'] = no_display_updates
    if screenshot is not None:
        params['screenshot'] = screenshot.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'HeadlessExperimental.beginFrame',
        'params': params,
    }
    json = yield cmd_dict
    result: T_JSON_DICT = {
        'hasDamage': bool(json['hasDamage']),
    }
    if 'screenshotData' in json:
        result['screenshotData'] = str(json['screenshotData'])
    return result


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Disables headless events for the target.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'HeadlessExperimental.disable',
    }
    json = yield cmd_dict


def enable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enables headless events for the target.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'HeadlessExperimental.enable',
    }
    json = yield cmd_dict


