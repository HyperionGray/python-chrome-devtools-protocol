"""
Browser Control Module

High-level browser automation API built on top of the CDP domain modules and
``CDPConnection``. This module provides Playwright-style helpers for common
browser automation tasks: element selection, clicking, typing, waiting,
navigation, and screenshots.

All methods in this module are coroutines that require a connected
``CDPConnection`` instance.

Example::

    import asyncio
    from cdp.connection import CDPConnection
    from cdp import browser_control as bc

    async def main():
        async with CDPConnection("ws://localhost:9222/devtools/page/ID") as conn:
            await bc.navigate(conn, "https://example.com")
            await bc.wait_for_load(conn)

            node = await bc.query_selector(conn, "h1")
            text = await bc.get_text(conn, node)
            print(text)

            await bc.click(conn, "a")
            await bc.type_text(conn, "input[name='q']", "hello world")
            data = await bc.screenshot(conn)
            with open("page.png", "wb") as f:
                f.write(data)

    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import base64
import typing

from cdp import dom, input_, page, runtime
from cdp.connection import CDPConnection

__all__ = [
    # Navigation
    "navigate",
    "reload",
    "go_back",
    "go_forward",
    "wait_for_load",
    # Element selection
    "query_selector",
    "query_selector_all",
    # Element interaction
    "click",
    "double_click",
    "hover",
    "type_text",
    "clear_and_type",
    "press_key",
    "focus",
    "select_option",
    # Element inspection
    "get_text",
    "get_attribute",
    "get_bounding_box",
    "is_visible",
    # Screenshots
    "screenshot",
    "screenshot_element",
    # JavaScript
    "evaluate",
    "evaluate_on_node",
    # Waiting
    "wait_for_selector",
    "wait_for_event",
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _get_document_node(conn: CDPConnection) -> dom.NodeId:
    """Return the root document NodeId."""
    document = await conn.execute(dom.get_document(depth=0))
    return document.node_id


async def _resolve_node_center(
    conn: CDPConnection, node_id: dom.NodeId
) -> typing.Tuple[float, float]:
    """Return the (x, y) centre of a DOM node's bounding box."""
    box = await conn.execute(dom.get_box_model(node_id=node_id))
    content = box.content  # Quad – flat list of 8 floats: x0,y0 x1,y1 x2,y2 x3,y3
    xs = content[0::2]
    ys = content[1::2]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    return cx, cy


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

async def navigate(conn: CDPConnection, url: str, timeout: float = 30.0) -> page.FrameId:
    """Navigate the current page to *url*.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param url: Destination URL.
    :param timeout: Maximum seconds to wait for the navigation command.
    :returns: The :class:`~cdp.page.FrameId` of the navigated frame.
    :raises cdp.connection.CDPCommandError: If navigation fails.
    """
    result = await conn.execute(page.navigate(url=url), timeout=timeout)
    frame_id: page.FrameId = result[0]
    return frame_id


async def reload(conn: CDPConnection, ignore_cache: bool = False) -> None:
    """Reload the current page.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param ignore_cache: When ``True`` bypass the browser cache (hard reload).
    """
    await conn.execute(page.reload(ignore_cache=ignore_cache))


async def go_back(conn: CDPConnection) -> bool:
    """Navigate back in history.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :returns: ``True`` if a back entry existed, ``False`` otherwise.
    """
    index, entries = await conn.execute(page.get_navigation_history())
    if index > 0:
        entry = entries[index - 1]
        await conn.execute(page.navigate_to_history_entry(entry_id=entry.id_))
        return True
    return False


async def go_forward(conn: CDPConnection) -> bool:
    """Navigate forward in history.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :returns: ``True`` if a forward entry existed, ``False`` otherwise.
    """
    index, entries = await conn.execute(page.get_navigation_history())
    if index < len(entries) - 1:
        entry = entries[index + 1]
        await conn.execute(page.navigate_to_history_entry(entry_id=entry.id_))
        return True
    return False


async def wait_for_load(
    conn: CDPConnection,
    timeout: float = 30.0,
) -> None:
    """Wait until the page fires a ``Page.loadEventFired`` event.

    You must have called ``await conn.execute(page.enable())`` before using
    this helper so that page events are delivered.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param timeout: Maximum seconds to wait.
    :raises asyncio.TimeoutError: If the page does not load within *timeout*.
    """
    await wait_for_event(conn, page.LoadEventFired, timeout=timeout)


# ---------------------------------------------------------------------------
# Element selection
# ---------------------------------------------------------------------------

async def query_selector(
    conn: CDPConnection,
    selector: str,
    root: typing.Optional[dom.NodeId] = None,
) -> dom.NodeId:
    """Return the :class:`~cdp.dom.NodeId` of the first element matching
    *selector* within *root* (defaults to the document root).

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector: CSS selector string.
    :param root: Optional root node; defaults to the document root.
    :returns: Matched :class:`~cdp.dom.NodeId`.
    :raises ValueError: If no element matches the selector.
    """
    if root is None:
        root = await _get_document_node(conn)
    node_id = await conn.execute(dom.query_selector(node_id=root, selector=selector))
    if node_id == 0:
        raise ValueError(f"No element found for selector: {selector!r}")
    return node_id


async def query_selector_all(
    conn: CDPConnection,
    selector: str,
    root: typing.Optional[dom.NodeId] = None,
) -> typing.List[dom.NodeId]:
    """Return all :class:`~cdp.dom.NodeId` values matching *selector*.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector: CSS selector string.
    :param root: Optional root node; defaults to the document root.
    :returns: List of matched :class:`~cdp.dom.NodeId` values (may be empty).
    """
    if root is None:
        root = await _get_document_node(conn)
    return await conn.execute(dom.query_selector_all(node_id=root, selector=selector))


# ---------------------------------------------------------------------------
# Element interaction
# ---------------------------------------------------------------------------

async def click(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
    button: str = "left",
    click_count: int = 1,
) -> None:
    """Click the element identified by *selector_or_node*.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    :param button: Mouse button – ``"left"``, ``"right"``, or ``"middle"``.
    :param click_count: Number of clicks (use ``2`` for double-click).
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    # Scroll node into view first so coordinates are correct.
    await conn.execute(dom.scroll_into_view_if_needed(node_id=node))
    cx, cy = await _resolve_node_center(conn, node)
    _btn = input_.MouseButton(button)
    for event_type in ("mouseMoved", "mousePressed", "mouseReleased"):
        await conn.execute(
            input_.dispatch_mouse_event(
                type_=event_type,
                x=cx,
                y=cy,
                button=_btn,
                click_count=click_count,
            )
        )


async def double_click(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
) -> None:
    """Double-click the element identified by *selector_or_node*.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    """
    await click(conn, selector_or_node, button="left", click_count=2)


async def hover(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
) -> None:
    """Move the mouse pointer over the element identified by *selector_or_node*.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    await conn.execute(dom.scroll_into_view_if_needed(node_id=node))
    cx, cy = await _resolve_node_center(conn, node)
    await conn.execute(
        input_.dispatch_mouse_event(type_="mouseMoved", x=cx, y=cy)
    )


async def type_text(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
    text: str,
    delay: float = 0.0,
) -> None:
    """Focus the element and type *text* into it, character by character.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    :param text: Text to type.
    :param delay: Optional delay in seconds between keystrokes.
    """
    await focus(conn, selector_or_node)
    for char in text:
        await conn.execute(
            input_.dispatch_key_event(type_="keyDown", text=char, key=char)
        )
        await conn.execute(
            input_.dispatch_key_event(type_="keyUp", text=char, key=char)
        )
        if delay > 0:
            await asyncio.sleep(delay)


async def clear_and_type(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
    text: str,
    delay: float = 0.0,
) -> None:
    """Select all existing text in the element, then type *text*.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    :param text: Replacement text.
    :param delay: Optional delay in seconds between keystrokes.
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    await focus(conn, node)
    # Select all – platform-agnostic via JavaScript.
    await conn.execute(
        runtime.evaluate(expression="document.execCommand('selectAll', false, null)")
    )
    await type_text(conn, node, text, delay=delay)


async def press_key(
    conn: CDPConnection,
    key: str,
    modifiers: int = 0,
) -> None:
    """Simulate pressing a single keyboard key.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param key: DOM key name, e.g. ``"Enter"``, ``"Tab"``, ``"Escape"``,
        ``"ArrowDown"``, or a single character like ``"a"``.
    :param modifiers: Bit-field of modifier keys
        (Alt=1, Ctrl=2, Meta=4, Shift=8).
    """
    for event_type in ("keyDown", "keyUp"):
        await conn.execute(
            input_.dispatch_key_event(
                type_=event_type,
                key=key,
                modifiers=modifiers,
            )
        )


async def focus(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
) -> None:
    """Move keyboard focus to the element identified by *selector_or_node*.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    await conn.execute(dom.focus(node_id=node))


async def select_option(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
    value: str,
) -> None:
    """Select the ``<option>`` with the given *value* inside a ``<select>`` element.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector for the ``<select>`` element.
    :param value: The ``value`` attribute of the ``<option>`` to select.
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    obj = await conn.execute(dom.resolve_node(node_id=node))
    if obj is None:
        raise ValueError("Could not resolve node to a remote object")
    escaped = value.replace("'", "\\'")
    expr = f"function() {{ this.value = '{escaped}'; this.dispatchEvent(new Event('change', {{bubbles: true}})); }}"
    await conn.execute(
        runtime.call_function_on(
            function_declaration=expr,
            object_id=obj.object_id,
        )
    )


# ---------------------------------------------------------------------------
# Element inspection
# ---------------------------------------------------------------------------

async def get_text(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
) -> str:
    """Return the ``innerText`` of the element.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    :returns: The ``innerText`` value (empty string if not available).
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    obj = await conn.execute(dom.resolve_node(node_id=node))
    if obj is None or obj.object_id is None:
        return ""
    text_result, text_exc = await conn.execute(
        runtime.call_function_on(
            function_declaration="function() { return this.innerText || this.textContent || ''; }",
            object_id=obj.object_id,
        )
    )
    if text_exc is not None:
        return ""
    return str(text_result.value) if text_result and text_result.value is not None else ""


async def get_attribute(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
    attribute: str,
) -> typing.Optional[str]:
    """Return the value of *attribute* on the element, or ``None`` if absent.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    :param attribute: Attribute name, e.g. ``"href"``, ``"class"``, ``"value"``.
    :returns: Attribute value or ``None``.
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    attrs = await conn.execute(dom.get_attributes(node_id=node))
    # attrs is a flat list: [name, value, name, value, ...]
    it = iter(attrs)
    mapping = dict(zip(it, it))
    return mapping.get(attribute)


async def get_bounding_box(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
) -> typing.Dict[str, float]:
    """Return the bounding box of an element as a dict with keys
    ``x``, ``y``, ``width``, ``height``.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    :returns: Dict with bounding-box information.
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    box = await conn.execute(dom.get_box_model(node_id=node))
    content = box.content
    xs = content[0::2]
    ys = content[1::2]
    return {
        "x": min(xs),
        "y": min(ys),
        "width": max(xs) - min(xs),
        "height": max(ys) - min(ys),
    }


async def is_visible(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
) -> bool:
    """Return ``True`` if the element is visible on screen.

    Visibility is determined by checking that the element's bounding box has
    a non-zero area and that the CSS ``visibility`` / ``display`` properties
    do not hide it.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    try:
        box = await conn.execute(dom.get_box_model(node_id=node))
    except Exception:
        return False
    content = box.content
    xs = content[0::2]
    ys = content[1::2]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    if width <= 0 or height <= 0:
        return False
    obj = await conn.execute(dom.resolve_node(node_id=node))
    if obj is None or obj.object_id is None:
        return False
    vis_result, vis_exc = await conn.execute(
        runtime.call_function_on(
            function_declaration=(
                "function() {"
                "  var style = window.getComputedStyle(this);"
                "  return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';"
                "}"
            ),
            object_id=obj.object_id,
        )
    )
    if vis_exc is not None:
        return False
    return bool(vis_result.value) if vis_result else False


# ---------------------------------------------------------------------------
# Screenshots
# ---------------------------------------------------------------------------

async def screenshot(
    conn: CDPConnection,
    format_: str = "png",
    quality: typing.Optional[int] = None,
    full_page: bool = False,
) -> bytes:
    """Capture a screenshot of the current viewport.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param format_: Image format – ``"png"`` (default) or ``"jpeg"``.
    :param quality: JPEG quality ``0``–``100`` (ignored for PNG).
    :param full_page: When ``True``, capture the full scrollable page.
    :returns: Raw image data as :class:`bytes`.
    """
    data_b64: str = await conn.execute(
        page.capture_screenshot(
            format_=format_,
            quality=quality,
            capture_beyond_viewport=full_page,
        )
    )
    return base64.b64decode(data_b64)


async def screenshot_element(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
    format_: str = "png",
    quality: typing.Optional[int] = None,
) -> bytes:
    """Capture a screenshot clipped to a specific element.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    :param format_: Image format – ``"png"`` (default) or ``"jpeg"``.
    :param quality: JPEG quality ``0``–``100`` (ignored for PNG).
    :returns: Raw image data as :class:`bytes`.
    """
    bbox = await get_bounding_box(conn, selector_or_node)
    clip = page.Viewport(
        x=bbox["x"],
        y=bbox["y"],
        width=bbox["width"],
        height=bbox["height"],
        scale=1.0,
    )
    data_b64: str = await conn.execute(
        page.capture_screenshot(format_=format_, quality=quality, clip=clip)
    )
    return base64.b64decode(data_b64)


# ---------------------------------------------------------------------------
# JavaScript evaluation
# ---------------------------------------------------------------------------

async def evaluate(
    conn: CDPConnection,
    expression: str,
    await_promise: bool = False,
) -> typing.Any:
    """Evaluate a JavaScript *expression* in the page context.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param expression: JavaScript expression to evaluate.
    :param await_promise: When ``True``, await a returned Promise.
    :returns: The primitive value returned by the expression, or ``None``.
    :raises RuntimeError: If the expression throws a JavaScript exception.
    """
    result, exc = await conn.execute(
        runtime.evaluate(expression=expression, await_promise=await_promise)
    )
    if exc is not None:
        raise RuntimeError(
            f"JavaScript exception: {exc.text}"
        )
    return result.value if result else None


async def evaluate_on_node(
    conn: CDPConnection,
    selector_or_node: typing.Union[str, dom.NodeId],
    function_declaration: str,
) -> typing.Any:
    """Call a JavaScript function with the matched element as ``this``.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector_or_node: CSS selector string or a :class:`~cdp.dom.NodeId`.
    :param function_declaration: JavaScript function body, e.g.
        ``"function() { return this.value; }"``.
    :returns: The primitive return value, or ``None``.
    :raises RuntimeError: If the function throws a JavaScript exception.
    """
    node = (
        await query_selector(conn, selector_or_node)
        if isinstance(selector_or_node, str)
        else selector_or_node
    )
    obj = await conn.execute(dom.resolve_node(node_id=node))
    if obj is None or obj.object_id is None:
        raise ValueError("Could not resolve node to a remote object")
    result, exc = await conn.execute(
        runtime.call_function_on(
            function_declaration=function_declaration,
            object_id=obj.object_id,
        )
    )
    if exc is not None:
        raise RuntimeError(f"JavaScript exception: {exc.text}")
    return result.value if result else None


# ---------------------------------------------------------------------------
# Waiting
# ---------------------------------------------------------------------------

async def wait_for_selector(
    conn: CDPConnection,
    selector: str,
    timeout: float = 30.0,
    poll_interval: float = 0.25,
    root: typing.Optional[dom.NodeId] = None,
) -> dom.NodeId:
    """Poll until *selector* matches an element in the DOM.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param selector: CSS selector string.
    :param timeout: Maximum seconds to wait.
    :param poll_interval: Polling interval in seconds.
    :param root: Optional root node; defaults to the document root.
    :returns: The matched :class:`~cdp.dom.NodeId`.
    :raises asyncio.TimeoutError: If no element appears within *timeout*.
    """
    deadline = asyncio.get_event_loop().time() + timeout
    while True:
        try:
            node_id = await query_selector(conn, selector, root=root)
            return node_id
        except ValueError:
            pass
        if asyncio.get_event_loop().time() >= deadline:
            raise asyncio.TimeoutError(
                f"Timed out waiting for selector {selector!r} ({timeout}s)"
            )
        await asyncio.sleep(poll_interval)


_T_Event = typing.TypeVar("_T_Event")


async def wait_for_event(
    conn: CDPConnection,
    event_type: typing.Type[_T_Event],
    timeout: float = 30.0,
) -> _T_Event:
    """Wait for a specific CDP event type to be received.

    :param conn: An open :class:`~cdp.connection.CDPConnection`.
    :param event_type: The CDP event class to wait for, e.g.
        :class:`~cdp.page.LoadEventFired`.
    :param timeout: Maximum seconds to wait.
    :returns: The received event instance.
    :raises asyncio.TimeoutError: If the event is not received within *timeout*.
    """
    async def _wait() -> _T_Event:
        async for event in conn.listen():
            if isinstance(event, event_type):
                return event  # type: ignore[return-value]
        raise CDPConnectionError("Connection closed before event arrived")  # noqa: F821

    try:
        from cdp.connection import CDPConnectionError  # local import to avoid circular
        return await asyncio.wait_for(_wait(), timeout=timeout)
    except asyncio.TimeoutError:
        raise asyncio.TimeoutError(
            f"Timed out waiting for event {event_type.__name__} ({timeout}s)"
        )
