'''
DO NOT EDIT THIS FILE

This file is generated from the CDP definitions. If you need to make changes,
edit the generator and regenerate all of the modules.

Domain: page
Experimental: False
'''

from cdp.util import T_JSON_DICT
from dataclasses import dataclass
import enum
import typing

from .types import *
from ..dom import types as dom
from ..debugger import types as debugger
from ..emulation import types as emulation
from ..network import types as network
from ..runtime import types as runtime



def add_script_to_evaluate_on_load(
        script_source: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,ScriptIdentifier]:
    '''
    Deprecated, please use addScriptToEvaluateOnNewDocument instead.
    
    :param script_source: 
    :returns: Identifier of the added script.
    '''
    params: T_JSON_DICT = {
        'scriptSource': script_source,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.addScriptToEvaluateOnLoad',
        'params': params,
    }
    json = yield cmd_dict
    return ScriptIdentifier.from_json(json['identifier'])


def add_script_to_evaluate_on_new_document(
        source: str,
        world_name: typing.Optional[str] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,ScriptIdentifier]:
    '''
    Evaluates given script in every frame upon creation (before loading frame's scripts).
    
    :param source: 
    :param world_name: If specified, creates an isolated world with the given name and evaluates given script in it.
    This world name will be used as the ExecutionContextDescription::name when the corresponding
    event is emitted.
    :returns: Identifier of the added script.
    '''
    params: T_JSON_DICT = {
        'source': source,
    }
    if world_name is not None:
        params['worldName'] = world_name
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.addScriptToEvaluateOnNewDocument',
        'params': params,
    }
    json = yield cmd_dict
    return ScriptIdentifier.from_json(json['identifier'])


def bring_to_front() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Brings page to front (activates tab).
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.bringToFront',
    }
    json = yield cmd_dict


def capture_screenshot(
        format: typing.Optional[str] = None,
        quality: typing.Optional[int] = None,
        clip: typing.Optional[Viewport] = None,
        from_surface: typing.Optional[bool] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,str]:
    '''
    Capture page screenshot.
    
    :param format: Image compression format (defaults to png).
    :param quality: Compression quality from range [0..100] (jpeg only).
    :param clip: Capture the screenshot of a given region only.
    :param from_surface: Capture the screenshot from the surface, rather than the view. Defaults to true.
    :returns: Base64-encoded image data.
    '''
    params: T_JSON_DICT = {
    }
    if format is not None:
        params['format'] = format
    if quality is not None:
        params['quality'] = quality
    if clip is not None:
        params['clip'] = clip.to_json()
    if from_surface is not None:
        params['fromSurface'] = from_surface
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.captureScreenshot',
        'params': params,
    }
    json = yield cmd_dict
    return str(json['data'])


def capture_snapshot(
        format: typing.Optional[str] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,str]:
    '''
    Returns a snapshot of the page as a string. For MHTML format, the serialization includes
    iframes, shadow DOM, external resources, and element-inline styles.
    
    :param format: Format (defaults to mhtml).
    :returns: Serialized page data.
    '''
    params: T_JSON_DICT = {
    }
    if format is not None:
        params['format'] = format
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.captureSnapshot',
        'params': params,
    }
    json = yield cmd_dict
    return str(json['data'])


def clear_device_metrics_override() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Clears the overriden device metrics.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.clearDeviceMetricsOverride',
    }
    json = yield cmd_dict


def clear_device_orientation_override() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Clears the overridden Device Orientation.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.clearDeviceOrientationOverride',
    }
    json = yield cmd_dict


def clear_geolocation_override() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Clears the overriden Geolocation Position and Error.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.clearGeolocationOverride',
    }
    json = yield cmd_dict


def create_isolated_world(
        frame_id: FrameId,
        world_name: typing.Optional[str] = None,
        grant_univeral_access: typing.Optional[bool] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,runtime.ExecutionContextId]:
    '''
    Creates an isolated world for the given frame.
    
    :param frame_id: Id of the frame in which the isolated world should be created.
    :param world_name: An optional name which is reported in the Execution Context.
    :param grant_univeral_access: Whether or not universal access should be granted to the isolated world. This is a powerful
    option, use with caution.
    :returns: Execution context of the isolated world.
    '''
    params: T_JSON_DICT = {
        'frameId': frame_id.to_json(),
    }
    if world_name is not None:
        params['worldName'] = world_name
    if grant_univeral_access is not None:
        params['grantUniveralAccess'] = grant_univeral_access
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.createIsolatedWorld',
        'params': params,
    }
    json = yield cmd_dict
    return runtime.ExecutionContextId.from_json(json['executionContextId'])


def delete_cookie(
        cookie_name: str,
        url: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Deletes browser cookie with given name, domain and path.
    
    :param cookie_name: Name of the cookie to remove.
    :param url: URL to match cooke domain and path.
    '''
    params: T_JSON_DICT = {
        'cookieName': cookie_name,
        'url': url,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.deleteCookie',
        'params': params,
    }
    json = yield cmd_dict


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Disables page domain notifications.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.disable',
    }
    json = yield cmd_dict


def enable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enables page domain notifications.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.enable',
    }
    json = yield cmd_dict


def get_app_manifest() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,dict]:
    '''
    
    :returns: a dict with the following keys:
        * url: Manifest location.
        * errors: 
        * data: (Optional) Manifest content.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.getAppManifest',
    }
    json = yield cmd_dict
    result: T_JSON_DICT = {
        'url': str(json['url']),
        'errors': [AppManifestError.from_json(i) for i in json['errors']],
    }
    if 'data' in json:
        result['data'] = str(json['data'])
    return result


def get_installability_errors() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List['str']]:
    '''
    
    :returns: 
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.getInstallabilityErrors',
    }
    json = yield cmd_dict
    return [str(i) for i in json['errors']]


def get_cookies() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List['network.Cookie']]:
    '''
    Returns all browser cookies. Depending on the backend support, will return detailed cookie
    information in the `cookies` field.
    :returns: Array of cookie objects.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.getCookies',
    }
    json = yield cmd_dict
    return [network.Cookie.from_json(i) for i in json['cookies']]


def get_frame_tree() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,FrameTree]:
    '''
    Returns present frame tree structure.
    :returns: Present frame tree structure.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.getFrameTree',
    }
    json = yield cmd_dict
    return FrameTree.from_json(json['frameTree'])


def get_layout_metrics() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,dict]:
    '''
    Returns metrics relating to the layouting of the page, such as viewport bounds/scale.
    :returns: a dict with the following keys:
        * layoutViewport: Metrics relating to the layout viewport.
        * visualViewport: Metrics relating to the visual viewport.
        * contentSize: Size of scrollable area.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.getLayoutMetrics',
    }
    json = yield cmd_dict
    result: T_JSON_DICT = {
        'layoutViewport': LayoutViewport.from_json(json['layoutViewport']),
        'visualViewport': VisualViewport.from_json(json['visualViewport']),
        'contentSize': dom.Rect.from_json(json['contentSize']),
    }
    return result


def get_navigation_history() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,dict]:
    '''
    Returns navigation history for the current page.
    :returns: a dict with the following keys:
        * currentIndex: Index of the current navigation history entry.
        * entries: Array of navigation history entries.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.getNavigationHistory',
    }
    json = yield cmd_dict
    result: T_JSON_DICT = {
        'currentIndex': int(json['currentIndex']),
        'entries': [NavigationEntry.from_json(i) for i in json['entries']],
    }
    return result


def reset_navigation_history() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Resets navigation history for the current page.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.resetNavigationHistory',
    }
    json = yield cmd_dict


def get_resource_content(
        frame_id: FrameId,
        url: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,dict]:
    '''
    Returns content of the given resource.
    
    :param frame_id: Frame id to get resource for.
    :param url: URL of the resource to get content for.
    :returns: a dict with the following keys:
        * content: Resource content.
        * base64Encoded: True, if content was served as base64.
    '''
    params: T_JSON_DICT = {
        'frameId': frame_id.to_json(),
        'url': url,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.getResourceContent',
        'params': params,
    }
    json = yield cmd_dict
    result: T_JSON_DICT = {
        'content': str(json['content']),
        'base64Encoded': bool(json['base64Encoded']),
    }
    return result


def get_resource_tree() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,FrameResourceTree]:
    '''
    Returns present frame / resource tree structure.
    :returns: Present frame / resource tree structure.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.getResourceTree',
    }
    json = yield cmd_dict
    return FrameResourceTree.from_json(json['frameTree'])


def handle_java_script_dialog(
        accept: bool,
        prompt_text: typing.Optional[str] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Accepts or dismisses a JavaScript initiated dialog (alert, confirm, prompt, or onbeforeunload).
    
    :param accept: Whether to accept or dismiss the dialog.
    :param prompt_text: The text to enter into the dialog prompt before accepting. Used only if this is a prompt
    dialog.
    '''
    params: T_JSON_DICT = {
        'accept': accept,
    }
    if prompt_text is not None:
        params['promptText'] = prompt_text
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.handleJavaScriptDialog',
        'params': params,
    }
    json = yield cmd_dict


def navigate(
        url: str,
        referrer: typing.Optional[str] = None,
        transition_type: typing.Optional[TransitionType] = None,
        frame_id: typing.Optional[FrameId] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,dict]:
    '''
    Navigates current page to the given URL.
    
    :param url: URL to navigate the page to.
    :param referrer: Referrer URL.
    :param transition_type: Intended transition type.
    :param frame_id: Frame id to navigate, if not specified navigates the top frame.
    :returns: a dict with the following keys:
        * frameId: Frame id that has navigated (or failed to navigate)
        * loaderId: (Optional) Loader identifier.
        * errorText: (Optional) User friendly error message, present if and only if navigation has failed.
    '''
    params: T_JSON_DICT = {
        'url': url,
    }
    if referrer is not None:
        params['referrer'] = referrer
    if transition_type is not None:
        params['transitionType'] = transition_type.to_json()
    if frame_id is not None:
        params['frameId'] = frame_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.navigate',
        'params': params,
    }
    json = yield cmd_dict
    result: T_JSON_DICT = {
        'frameId': FrameId.from_json(json['frameId']),
    }
    if 'loaderId' in json:
        result['loaderId'] = network.LoaderId.from_json(json['loaderId'])
    if 'errorText' in json:
        result['errorText'] = str(json['errorText'])
    return result


def navigate_to_history_entry(
        entry_id: int,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Navigates current page to the given history entry.
    
    :param entry_id: Unique id of the entry to navigate to.
    '''
    params: T_JSON_DICT = {
        'entryId': entry_id,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.navigateToHistoryEntry',
        'params': params,
    }
    json = yield cmd_dict


def print_to_pdf(
        landscape: typing.Optional[bool] = None,
        display_header_footer: typing.Optional[bool] = None,
        print_background: typing.Optional[bool] = None,
        scale: typing.Optional[float] = None,
        paper_width: typing.Optional[float] = None,
        paper_height: typing.Optional[float] = None,
        margin_top: typing.Optional[float] = None,
        margin_bottom: typing.Optional[float] = None,
        margin_left: typing.Optional[float] = None,
        margin_right: typing.Optional[float] = None,
        page_ranges: typing.Optional[str] = None,
        ignore_invalid_page_ranges: typing.Optional[bool] = None,
        header_template: typing.Optional[str] = None,
        footer_template: typing.Optional[str] = None,
        prefer_css_page_size: typing.Optional[bool] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,str]:
    '''
    Print page as PDF.
    
    :param landscape: Paper orientation. Defaults to false.
    :param display_header_footer: Display header and footer. Defaults to false.
    :param print_background: Print background graphics. Defaults to false.
    :param scale: Scale of the webpage rendering. Defaults to 1.
    :param paper_width: Paper width in inches. Defaults to 8.5 inches.
    :param paper_height: Paper height in inches. Defaults to 11 inches.
    :param margin_top: Top margin in inches. Defaults to 1cm (~0.4 inches).
    :param margin_bottom: Bottom margin in inches. Defaults to 1cm (~0.4 inches).
    :param margin_left: Left margin in inches. Defaults to 1cm (~0.4 inches).
    :param margin_right: Right margin in inches. Defaults to 1cm (~0.4 inches).
    :param page_ranges: Paper ranges to print, e.g., '1-5, 8, 11-13'. Defaults to the empty string, which means
    print all pages.
    :param ignore_invalid_page_ranges: Whether to silently ignore invalid but successfully parsed page ranges, such as '3-2'.
    Defaults to false.
    :param header_template: HTML template for the print header. Should be valid HTML markup with following
    classes used to inject printing values into them:
    - `date`: formatted print date
    - `title`: document title
    - `url`: document location
    - `pageNumber`: current page number
    - `totalPages`: total pages in the document
    
    For example, `<span class=title></span>` would generate span containing the title.
    :param footer_template: HTML template for the print footer. Should use the same format as the `headerTemplate`.
    :param prefer_css_page_size: Whether or not to prefer page size as defined by css. Defaults to false,
    in which case the content will be scaled to fit the paper size.
    :returns: Base64-encoded pdf data.
    '''
    params: T_JSON_DICT = {
    }
    if landscape is not None:
        params['landscape'] = landscape
    if display_header_footer is not None:
        params['displayHeaderFooter'] = display_header_footer
    if print_background is not None:
        params['printBackground'] = print_background
    if scale is not None:
        params['scale'] = scale
    if paper_width is not None:
        params['paperWidth'] = paper_width
    if paper_height is not None:
        params['paperHeight'] = paper_height
    if margin_top is not None:
        params['marginTop'] = margin_top
    if margin_bottom is not None:
        params['marginBottom'] = margin_bottom
    if margin_left is not None:
        params['marginLeft'] = margin_left
    if margin_right is not None:
        params['marginRight'] = margin_right
    if page_ranges is not None:
        params['pageRanges'] = page_ranges
    if ignore_invalid_page_ranges is not None:
        params['ignoreInvalidPageRanges'] = ignore_invalid_page_ranges
    if header_template is not None:
        params['headerTemplate'] = header_template
    if footer_template is not None:
        params['footerTemplate'] = footer_template
    if prefer_css_page_size is not None:
        params['preferCSSPageSize'] = prefer_css_page_size
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.printToPDF',
        'params': params,
    }
    json = yield cmd_dict
    return str(json['data'])


def reload(
        ignore_cache: typing.Optional[bool] = None,
        script_to_evaluate_on_load: typing.Optional[str] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Reloads given page optionally ignoring the cache.
    
    :param ignore_cache: If true, browser cache is ignored (as if the user pressed Shift+refresh).
    :param script_to_evaluate_on_load: If set, the script will be injected into all frames of the inspected page after reload.
    Argument will be ignored if reloading dataURL origin.
    '''
    params: T_JSON_DICT = {
    }
    if ignore_cache is not None:
        params['ignoreCache'] = ignore_cache
    if script_to_evaluate_on_load is not None:
        params['scriptToEvaluateOnLoad'] = script_to_evaluate_on_load
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.reload',
        'params': params,
    }
    json = yield cmd_dict


def remove_script_to_evaluate_on_load(
        identifier: ScriptIdentifier,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Deprecated, please use removeScriptToEvaluateOnNewDocument instead.
    
    :param identifier: 
    '''
    params: T_JSON_DICT = {
        'identifier': identifier.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.removeScriptToEvaluateOnLoad',
        'params': params,
    }
    json = yield cmd_dict


def remove_script_to_evaluate_on_new_document(
        identifier: ScriptIdentifier,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Removes given script from the list.
    
    :param identifier: 
    '''
    params: T_JSON_DICT = {
        'identifier': identifier.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.removeScriptToEvaluateOnNewDocument',
        'params': params,
    }
    json = yield cmd_dict


def screencast_frame_ack(
        session_id: int,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Acknowledges that a screencast frame has been received by the frontend.
    
    :param session_id: Frame number.
    '''
    params: T_JSON_DICT = {
        'sessionId': session_id,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.screencastFrameAck',
        'params': params,
    }
    json = yield cmd_dict


def search_in_resource(
        frame_id: FrameId,
        url: str,
        query: str,
        case_sensitive: typing.Optional[bool] = None,
        is_regex: typing.Optional[bool] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List['debugger.SearchMatch']]:
    '''
    Searches for given string in resource content.
    
    :param frame_id: Frame id for resource to search in.
    :param url: URL of the resource to search in.
    :param query: String to search for.
    :param case_sensitive: If true, search is case sensitive.
    :param is_regex: If true, treats string parameter as regex.
    :returns: List of search matches.
    '''
    params: T_JSON_DICT = {
        'frameId': frame_id.to_json(),
        'url': url,
        'query': query,
    }
    if case_sensitive is not None:
        params['caseSensitive'] = case_sensitive
    if is_regex is not None:
        params['isRegex'] = is_regex
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.searchInResource',
        'params': params,
    }
    json = yield cmd_dict
    return [debugger.SearchMatch.from_json(i) for i in json['result']]


def set_ad_blocking_enabled(
        enabled: bool,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enable Chrome's experimental ad filter on all sites.
    
    :param enabled: Whether to block ads.
    '''
    params: T_JSON_DICT = {
        'enabled': enabled,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setAdBlockingEnabled',
        'params': params,
    }
    json = yield cmd_dict


def set_bypass_csp(
        enabled: bool,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enable page Content Security Policy by-passing.
    
    :param enabled: Whether to bypass page CSP.
    '''
    params: T_JSON_DICT = {
        'enabled': enabled,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setBypassCSP',
        'params': params,
    }
    json = yield cmd_dict


def set_device_metrics_override(
        width: int,
        height: int,
        device_scale_factor: float,
        mobile: bool,
        scale: typing.Optional[float] = None,
        screen_width: typing.Optional[int] = None,
        screen_height: typing.Optional[int] = None,
        position_x: typing.Optional[int] = None,
        position_y: typing.Optional[int] = None,
        dont_set_visible_size: typing.Optional[bool] = None,
        screen_orientation: typing.Optional[emulation.ScreenOrientation] = None,
        viewport: typing.Optional[Viewport] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Overrides the values of device screen dimensions (window.screen.width, window.screen.height,
    window.innerWidth, window.innerHeight, and "device-width"/"device-height"-related CSS media
    query results).
    
    :param width: Overriding width value in pixels (minimum 0, maximum 10000000). 0 disables the override.
    :param height: Overriding height value in pixels (minimum 0, maximum 10000000). 0 disables the override.
    :param device_scale_factor: Overriding device scale factor value. 0 disables the override.
    :param mobile: Whether to emulate mobile device. This includes viewport meta tag, overlay scrollbars, text
    autosizing and more.
    :param scale: Scale to apply to resulting view image.
    :param screen_width: Overriding screen width value in pixels (minimum 0, maximum 10000000).
    :param screen_height: Overriding screen height value in pixels (minimum 0, maximum 10000000).
    :param position_x: Overriding view X position on screen in pixels (minimum 0, maximum 10000000).
    :param position_y: Overriding view Y position on screen in pixels (minimum 0, maximum 10000000).
    :param dont_set_visible_size: Do not set visible view size, rely upon explicit setVisibleSize call.
    :param screen_orientation: Screen orientation override.
    :param viewport: The viewport dimensions and scale. If not set, the override is cleared.
    '''
    params: T_JSON_DICT = {
        'width': width,
        'height': height,
        'deviceScaleFactor': device_scale_factor,
        'mobile': mobile,
    }
    if scale is not None:
        params['scale'] = scale
    if screen_width is not None:
        params['screenWidth'] = screen_width
    if screen_height is not None:
        params['screenHeight'] = screen_height
    if position_x is not None:
        params['positionX'] = position_x
    if position_y is not None:
        params['positionY'] = position_y
    if dont_set_visible_size is not None:
        params['dontSetVisibleSize'] = dont_set_visible_size
    if screen_orientation is not None:
        params['screenOrientation'] = screen_orientation.to_json()
    if viewport is not None:
        params['viewport'] = viewport.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setDeviceMetricsOverride',
        'params': params,
    }
    json = yield cmd_dict


def set_device_orientation_override(
        alpha: float,
        beta: float,
        gamma: float,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Overrides the Device Orientation.
    
    :param alpha: Mock alpha
    :param beta: Mock beta
    :param gamma: Mock gamma
    '''
    params: T_JSON_DICT = {
        'alpha': alpha,
        'beta': beta,
        'gamma': gamma,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setDeviceOrientationOverride',
        'params': params,
    }
    json = yield cmd_dict


def set_font_families(
        font_families: FontFamilies,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Set generic font families.
    
    :param font_families: Specifies font families to set. If a font family is not specified, it won't be changed.
    '''
    params: T_JSON_DICT = {
        'fontFamilies': font_families.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setFontFamilies',
        'params': params,
    }
    json = yield cmd_dict


def set_font_sizes(
        font_sizes: FontSizes,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Set default font sizes.
    
    :param font_sizes: Specifies font sizes to set. If a font size is not specified, it won't be changed.
    '''
    params: T_JSON_DICT = {
        'fontSizes': font_sizes.to_json(),
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setFontSizes',
        'params': params,
    }
    json = yield cmd_dict


def set_document_content(
        frame_id: FrameId,
        html: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Sets given markup as the document's HTML.
    
    :param frame_id: Frame id to set HTML for.
    :param html: HTML content to set.
    '''
    params: T_JSON_DICT = {
        'frameId': frame_id.to_json(),
        'html': html,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setDocumentContent',
        'params': params,
    }
    json = yield cmd_dict


def set_download_behavior(
        behavior: str,
        download_path: typing.Optional[str] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Set the behavior when downloading a file.
    
    :param behavior: Whether to allow all or deny all download requests, or use default Chrome behavior if
    available (otherwise deny).
    :param download_path: The default path to save downloaded files to. This is requred if behavior is set to 'allow'
    '''
    params: T_JSON_DICT = {
        'behavior': behavior,
    }
    if download_path is not None:
        params['downloadPath'] = download_path
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setDownloadBehavior',
        'params': params,
    }
    json = yield cmd_dict


def set_geolocation_override(
        latitude: typing.Optional[float] = None,
        longitude: typing.Optional[float] = None,
        accuracy: typing.Optional[float] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Overrides the Geolocation Position or Error. Omitting any of the parameters emulates position
    unavailable.
    
    :param latitude: Mock latitude
    :param longitude: Mock longitude
    :param accuracy: Mock accuracy
    '''
    params: T_JSON_DICT = {
    }
    if latitude is not None:
        params['latitude'] = latitude
    if longitude is not None:
        params['longitude'] = longitude
    if accuracy is not None:
        params['accuracy'] = accuracy
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setGeolocationOverride',
        'params': params,
    }
    json = yield cmd_dict


def set_lifecycle_events_enabled(
        enabled: bool,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Controls whether page will emit lifecycle events.
    
    :param enabled: If true, starts emitting lifecycle events.
    '''
    params: T_JSON_DICT = {
        'enabled': enabled,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setLifecycleEventsEnabled',
        'params': params,
    }
    json = yield cmd_dict


def set_touch_emulation_enabled(
        enabled: bool,
        configuration: typing.Optional[str] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Toggles mouse event-based touch event emulation.
    
    :param enabled: Whether the touch event emulation should be enabled.
    :param configuration: Touch/gesture events configuration. Default: current platform.
    '''
    params: T_JSON_DICT = {
        'enabled': enabled,
    }
    if configuration is not None:
        params['configuration'] = configuration
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setTouchEmulationEnabled',
        'params': params,
    }
    json = yield cmd_dict


def start_screencast(
        format: typing.Optional[str] = None,
        quality: typing.Optional[int] = None,
        max_width: typing.Optional[int] = None,
        max_height: typing.Optional[int] = None,
        every_nth_frame: typing.Optional[int] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Starts sending each frame using the `screencastFrame` event.
    
    :param format: Image compression format.
    :param quality: Compression quality from range [0..100].
    :param max_width: Maximum screenshot width.
    :param max_height: Maximum screenshot height.
    :param every_nth_frame: Send every n-th frame.
    '''
    params: T_JSON_DICT = {
    }
    if format is not None:
        params['format'] = format
    if quality is not None:
        params['quality'] = quality
    if max_width is not None:
        params['maxWidth'] = max_width
    if max_height is not None:
        params['maxHeight'] = max_height
    if every_nth_frame is not None:
        params['everyNthFrame'] = every_nth_frame
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.startScreencast',
        'params': params,
    }
    json = yield cmd_dict


def stop_loading() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Force the page stop all navigations and pending resource fetches.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.stopLoading',
    }
    json = yield cmd_dict


def crash() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Crashes renderer on the IO thread, generates minidumps.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.crash',
    }
    json = yield cmd_dict


def close() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Tries to close page, running its beforeunload hooks, if any.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.close',
    }
    json = yield cmd_dict


def set_web_lifecycle_state(
        state: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Tries to update the web lifecycle state of the page.
    It will transition the page to the given state according to:
    https://github.com/WICG/web-lifecycle/
    
    :param state: Target lifecycle state
    '''
    params: T_JSON_DICT = {
        'state': state,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setWebLifecycleState',
        'params': params,
    }
    json = yield cmd_dict


def stop_screencast() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Stops sending each frame in the `screencastFrame`.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.stopScreencast',
    }
    json = yield cmd_dict


def set_produce_compilation_cache(
        enabled: bool,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Forces compilation cache to be generated for every subresource script.
    
    :param enabled: 
    '''
    params: T_JSON_DICT = {
        'enabled': enabled,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.setProduceCompilationCache',
        'params': params,
    }
    json = yield cmd_dict


def add_compilation_cache(
        url: str,
        data: str,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Seeds compilation cache for given url. Compilation cache does not survive
    cross-process navigation.
    
    :param url: 
    :param data: Base64-encoded data
    '''
    params: T_JSON_DICT = {
        'url': url,
        'data': data,
    }
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.addCompilationCache',
        'params': params,
    }
    json = yield cmd_dict


def clear_compilation_cache() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Clears seeded compilation cache.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.clearCompilationCache',
    }
    json = yield cmd_dict


def generate_test_report(
        message: str,
        group: typing.Optional[str] = None,
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Generates a report for testing.
    
    :param message: Message to be displayed in the report.
    :param group: Specifies the endpoint group to deliver the report to.
    '''
    params: T_JSON_DICT = {
        'message': message,
    }
    if group is not None:
        params['group'] = group
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.generateTestReport',
        'params': params,
    }
    json = yield cmd_dict


def wait_for_debugger() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Pauses page execution. Can be resumed using generic Runtime.runIfWaitingForDebugger.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Page.waitForDebugger',
    }
    json = yield cmd_dict


