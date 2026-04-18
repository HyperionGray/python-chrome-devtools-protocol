"""
Tests for cdp.browser_control module.

These tests mock CDPConnection so no real browser is needed.
"""
import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call

from cdp import dom, page, runtime
from cdp.browser_control import (
    navigate,
    reload,
    go_back,
    go_forward,
    query_selector,
    query_selector_all,
    click,
    double_click,
    hover,
    type_text,
    clear_and_type,
    press_key,
    focus,
    get_text,
    get_attribute,
    get_bounding_box,
    is_visible,
    screenshot,
    screenshot_element,
    evaluate,
    evaluate_on_node,
    wait_for_selector,
    wait_for_event,
)


# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------

def _make_conn(*side_effects):
    """Build a mock CDPConnection whose execute() returns values in order."""
    conn = MagicMock()
    conn.execute = AsyncMock(side_effect=list(side_effects))
    # listen() is an async generator – mock it properly when needed per test.
    return conn


# ---------------------------------------------------------------------------
# Navigation tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_navigate_returns_frame_id():
    frame_id = page.FrameId("frame-1")
    conn = _make_conn((frame_id, None, None, None))
    result = await navigate(conn, "https://example.com")
    assert result == frame_id
    conn.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_reload_calls_page_reload():
    conn = _make_conn(None)
    await reload(conn)
    conn.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_go_back_when_history_available():
    entry = page.NavigationEntry(
        id_=1,
        url="https://prev.com",
        user_typed_url="https://prev.com",
        title="Prev",
        transition_type=page.TransitionType.TYPED,
    )
    # get_navigation_history returns (index, entries)
    conn = _make_conn((1, [entry, MagicMock()]), None)
    result = await go_back(conn)
    assert result is True
    assert conn.execute.await_count == 2


@pytest.mark.asyncio
async def test_go_back_at_start_of_history():
    conn = _make_conn((0, [MagicMock()]))
    result = await go_back(conn)
    assert result is False
    conn.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_go_forward_when_history_available():
    entry_next = page.NavigationEntry(
        id_=2,
        url="https://next.com",
        user_typed_url="https://next.com",
        title="Next",
        transition_type=page.TransitionType.TYPED,
    )
    conn = _make_conn((0, [MagicMock(), entry_next]), None)
    result = await go_forward(conn)
    assert result is True
    assert conn.execute.await_count == 2


@pytest.mark.asyncio
async def test_go_forward_at_end_of_history():
    conn = _make_conn((1, [MagicMock(), MagicMock()]))
    result = await go_forward(conn)
    assert result is False
    conn.execute.assert_awaited_once()


# ---------------------------------------------------------------------------
# Element selection tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_query_selector_found():
    doc_node = dom.Node(
        node_id=dom.NodeId(1),
        backend_node_id=dom.BackendNodeId(1),
        node_type=9,
        node_name="#document",
        local_name="",
        node_value="",
    )
    target_node_id = dom.NodeId(42)
    conn = _make_conn(doc_node, target_node_id)
    result = await query_selector(conn, "h1")
    assert result == target_node_id


@pytest.mark.asyncio
async def test_query_selector_not_found_raises():
    doc_node = dom.Node(
        node_id=dom.NodeId(1),
        backend_node_id=dom.BackendNodeId(1),
        node_type=9,
        node_name="#document",
        local_name="",
        node_value="",
    )
    conn = _make_conn(doc_node, dom.NodeId(0))
    with pytest.raises(ValueError, match="No element found"):
        await query_selector(conn, ".missing")


@pytest.mark.asyncio
async def test_query_selector_all():
    doc_node = dom.Node(
        node_id=dom.NodeId(1),
        backend_node_id=dom.BackendNodeId(1),
        node_type=9,
        node_name="#document",
        local_name="",
        node_value="",
    )
    ids = [dom.NodeId(10), dom.NodeId(20)]
    conn = _make_conn(doc_node, ids)
    result = await query_selector_all(conn, "li")
    assert result == ids


@pytest.mark.asyncio
async def test_query_selector_with_explicit_root():
    """When a root NodeId is provided, get_document should NOT be called."""
    root = dom.NodeId(5)
    target = dom.NodeId(99)
    conn = _make_conn(target)
    result = await query_selector(conn, "span", root=root)
    assert result == target
    # Only one execute call: query_selector itself
    conn.execute.assert_awaited_once()


# ---------------------------------------------------------------------------
# Element interaction tests
# ---------------------------------------------------------------------------

def _make_box_model(x=10.0, y=20.0, w=100.0, h=50.0):
    """Create a minimal BoxModel whose content quad covers the given rect."""
    # Quad is [x0,y0, x1,y1, x2,y2, x3,y3] clockwise from top-left.
    quad = dom.Quad([x, y, x + w, y, x + w, y + h, x, y + h])
    return dom.BoxModel(
        content=quad,
        padding=quad,
        border=quad,
        margin=quad,
        width=int(w),
        height=int(h),
    )


@pytest.mark.asyncio
async def test_click_dispatches_mouse_events():
    doc_node = dom.Node(
        node_id=dom.NodeId(1),
        backend_node_id=dom.BackendNodeId(1),
        node_type=9,
        node_name="#document",
        local_name="",
        node_value="",
    )
    target_node = dom.NodeId(42)
    box = _make_box_model(10, 20, 100, 50)
    # Calls: get_document, query_selector, scroll_into_view, get_box_model,
    # dispatch_mouse_event x3
    conn = _make_conn(doc_node, target_node, None, box, None, None, None)
    await click(conn, "button")
    assert conn.execute.await_count == 7


@pytest.mark.asyncio
async def test_click_with_node_id_skips_selector():
    node = dom.NodeId(42)
    box = _make_box_model()
    # Calls: scroll_into_view, get_box_model, dispatch_mouse_event x3
    conn = _make_conn(None, box, None, None, None)
    await click(conn, node)
    assert conn.execute.await_count == 5


@pytest.mark.asyncio
async def test_hover_dispatches_mousemoved():
    node = dom.NodeId(7)
    box = _make_box_model()
    conn = _make_conn(None, box, None)
    await hover(conn, node)
    assert conn.execute.await_count == 3


@pytest.mark.asyncio
async def test_press_key_sends_keydown_and_keyup():
    conn = _make_conn(None, None)
    await press_key(conn, "Enter")
    assert conn.execute.await_count == 2


@pytest.mark.asyncio
async def test_type_text_sends_events_per_character():
    doc_node = dom.Node(
        node_id=dom.NodeId(1),
        backend_node_id=dom.BackendNodeId(1),
        node_type=9,
        node_name="#document",
        local_name="",
        node_value="",
    )
    target_node = dom.NodeId(5)
    text = "hi"
    # focus: get_document, query_selector, dom.focus
    # then 2 chars * 2 events = 4
    conn = _make_conn(doc_node, target_node, None, None, None, None, None)
    await type_text(conn, "input", text)
    # 3 (focus) + 4 (2 chars * 2 key events) = 7
    assert conn.execute.await_count == 7


# ---------------------------------------------------------------------------
# Element inspection tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_attribute_returns_value():
    doc_node = dom.Node(
        node_id=dom.NodeId(1),
        backend_node_id=dom.BackendNodeId(1),
        node_type=9,
        node_name="#document",
        local_name="",
        node_value="",
    )
    target_node = dom.NodeId(10)
    attrs = ["class", "hero", "href", "https://example.com"]
    conn = _make_conn(doc_node, target_node, attrs)
    result = await get_attribute(conn, "a", "href")
    assert result == "https://example.com"


@pytest.mark.asyncio
async def test_get_attribute_missing_returns_none():
    node = dom.NodeId(10)
    attrs = ["class", "hero"]
    conn = _make_conn(attrs)
    result = await get_attribute(conn, node, "href")
    assert result is None


@pytest.mark.asyncio
async def test_get_bounding_box():
    node = dom.NodeId(3)
    box = _make_box_model(x=5.0, y=10.0, w=200.0, h=80.0)
    conn = _make_conn(box)
    result = await get_bounding_box(conn, node)
    assert result["x"] == pytest.approx(5.0)
    assert result["y"] == pytest.approx(10.0)
    assert result["width"] == pytest.approx(200.0)
    assert result["height"] == pytest.approx(80.0)


@pytest.mark.asyncio
async def test_get_text_returns_inner_text():
    node = dom.NodeId(7)
    remote_obj = runtime.RemoteObject(type_="string", value="Hello World")
    remote_obj.object_id = runtime.RemoteObjectId("obj-1")
    text_remote = runtime.RemoteObject(type_="string", value="Hello World")
    conn = _make_conn(remote_obj, (text_remote, None))
    result = await get_text(conn, node)
    assert result == "Hello World"


# ---------------------------------------------------------------------------
# Screenshot tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_screenshot_decodes_base64():
    import base64
    raw = b"\x89PNG\r\n\x1a\n"  # fake PNG header
    b64 = base64.b64encode(raw).decode()
    conn = _make_conn(b64)
    result = await screenshot(conn)
    assert result == raw


@pytest.mark.asyncio
async def test_screenshot_element():
    import base64
    node = dom.NodeId(5)
    box = _make_box_model(x=0, y=0, w=100, h=50)
    raw = b"jpeg_data"
    b64 = base64.b64encode(raw).decode()
    conn = _make_conn(box, b64)
    result = await screenshot_element(conn, node, format_="jpeg")
    assert result == raw
    assert conn.execute.await_count == 2


# ---------------------------------------------------------------------------
# JavaScript evaluation tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_evaluate_returns_value():
    remote = runtime.RemoteObject(type_="number", value=42)
    conn = _make_conn((remote, None))
    result = await evaluate(conn, "1+1")
    assert result == 42


@pytest.mark.asyncio
async def test_evaluate_raises_on_exception():
    exc_details = runtime.ExceptionDetails(
        exception_id=1,
        text="SyntaxError",
        line_number=0,
        column_number=0,
    )
    conn = _make_conn((None, exc_details))
    with pytest.raises(RuntimeError, match="JavaScript exception"):
        await evaluate(conn, "throw new Error()")


@pytest.mark.asyncio
async def test_evaluate_on_node():
    node = dom.NodeId(9)
    remote_obj = runtime.RemoteObject(type_="object")
    remote_obj.object_id = runtime.RemoteObjectId("obj-2")
    text_remote = runtime.RemoteObject(type_="string", value="inner")
    conn = _make_conn(remote_obj, (text_remote, None))
    result = await evaluate_on_node(conn, node, "function() { return this.value; }")
    assert result == "inner"


# ---------------------------------------------------------------------------
# wait_for_selector tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_wait_for_selector_found_immediately():
    doc_node = dom.Node(
        node_id=dom.NodeId(1),
        backend_node_id=dom.BackendNodeId(1),
        node_type=9,
        node_name="#document",
        local_name="",
        node_value="",
    )
    target = dom.NodeId(55)
    conn = _make_conn(doc_node, target)
    result = await wait_for_selector(conn, "h2")
    assert result == target


@pytest.mark.asyncio
async def test_wait_for_selector_timeout():
    doc_node = dom.Node(
        node_id=dom.NodeId(1),
        backend_node_id=dom.BackendNodeId(1),
        node_type=9,
        node_name="#document",
        local_name="",
        node_value="",
    )
    # Always return NodeId(0) = not found; repeat enough times for the timeout
    _ENOUGH_ATTEMPTS = 20  # timeout=0.1s / poll_interval=0.05s → at most ~4 polls
    conn = MagicMock()
    conn.execute = AsyncMock(side_effect=[doc_node, dom.NodeId(0)] * _ENOUGH_ATTEMPTS)
    with pytest.raises(asyncio.TimeoutError):
        await wait_for_selector(conn, ".ghost", timeout=0.1, poll_interval=0.05)


# ---------------------------------------------------------------------------
# wait_for_event tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_wait_for_event_receives_correct_type():
    """wait_for_event should return the first matching event."""
    target_event = page.LoadEventFired(timestamp=123.0)
    other_event = page.FrameStoppedLoading(frame_id=page.FrameId("f1"))

    async def _fake_listen():
        yield other_event
        yield target_event

    conn = MagicMock()
    conn.listen = _fake_listen
    conn._closed = False

    result = await wait_for_event(conn, page.LoadEventFired, timeout=2.0)
    assert isinstance(result, page.LoadEventFired)
    assert result.timestamp == 123.0


@pytest.mark.asyncio
async def test_wait_for_event_timeout():
    async def _never_match():
        for _ in range(100):
            yield page.FrameStoppedLoading(frame_id=page.FrameId("f1"))
            await asyncio.sleep(0.02)

    conn = MagicMock()
    conn.listen = _never_match
    conn._closed = False

    with pytest.raises(asyncio.TimeoutError):
        await wait_for_event(conn, page.LoadEventFired, timeout=0.1)
