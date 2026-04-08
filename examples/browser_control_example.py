#!/usr/bin/env python3
"""
Browser Control Example

Demonstrates the cdp.browser_control high-level automation API.

Prerequisites:
    pip install chrome-devtools-protocol[io]

Start Chrome with remote debugging enabled:
    chrome --remote-debugging-port=9222 --headless

Get the WebSocket URL for a tab:
    curl http://localhost:9222/json

Then update CDP_URL below with the "webSocketDebuggerUrl" value and run:
    python examples/browser_control_example.py
"""

import asyncio
from cdp.connection import CDPConnection
from cdp import browser_control as bc
from cdp import page


# Replace with the "webSocketDebuggerUrl" from http://localhost:9222/json
# Example: "ws://localhost:9222/devtools/page/ABC123"
CDP_URL = "ws://localhost:9222/devtools/page/YOUR_PAGE_ID"


async def demo_navigation(conn: CDPConnection) -> None:
    """Navigate to a URL and wait for the page to load."""
    print("\n--- Navigation ---")
    await conn.execute(page.enable())
    frame_id = await bc.navigate(conn, "https://example.com")
    await bc.wait_for_load(conn)
    print(f"Navigated, frame_id={frame_id}")


async def demo_element_selection(conn: CDPConnection) -> None:
    """Query DOM elements with CSS selectors."""
    print("\n--- Element Selection ---")
    h1 = await bc.query_selector(conn, "h1")
    print(f"Found <h1> node: {h1!r}")

    all_links = await bc.query_selector_all(conn, "a")
    print(f"Found {len(all_links)} link(s)")


async def demo_text_and_attributes(conn: CDPConnection) -> None:
    """Read text content and attributes from elements."""
    print("\n--- Text & Attributes ---")
    text = await bc.get_text(conn, "h1")
    print(f"<h1> text: {text!r}")

    href = await bc.get_attribute(conn, "a", "href")
    print(f"First link href: {href!r}")

    bbox = await bc.get_bounding_box(conn, "h1")
    print(f"<h1> bounding box: {bbox}")

    visible = await bc.is_visible(conn, "h1")
    print(f"<h1> visible: {visible}")


async def demo_interaction(conn: CDPConnection) -> None:
    """Click elements and type into inputs."""
    print("\n--- Interaction ---")
    # Navigate to a page with a search form
    await conn.execute(page.enable())
    await bc.navigate(conn, "https://www.google.com")
    await bc.wait_for_load(conn)

    search_box = await bc.wait_for_selector(
        conn,
        "textarea[name='q']",
        timeout=10,
        state="visible",
    )
    await bc.click(conn, search_box)
    await bc.type_text(conn, search_box, "Python CDP", delay=0.05)
    await bc.press_key(conn, "Enter")
    # Wait for Google loading UI to disappear before proceeding.
    await bc.wait_for_selector(
        conn,
        "div[role='progressbar']",
        state="hidden",
        timeout=10,
    )
    print("Submitted search form")


async def demo_javascript(conn: CDPConnection) -> None:
    """Evaluate JavaScript in the page context."""
    print("\n--- JavaScript ---")
    title = await bc.evaluate(conn, "document.title")
    print(f"Page title via JS: {title!r}")

    link_count = await bc.evaluate(conn, "document.querySelectorAll('a').length")
    print(f"Link count via JS: {link_count}")


async def demo_screenshot(conn: CDPConnection) -> None:
    """Take screenshots of the full page and a specific element."""
    print("\n--- Screenshots ---")
    png = await bc.screenshot(conn)
    with open("/tmp/page.png", "wb") as fh:
        fh.write(png)
    print(f"Full-page screenshot saved ({len(png)} bytes) → /tmp/page.png")

    try:
        png_elem = await bc.screenshot_element(conn, "h1")
        with open("/tmp/h1.png", "wb") as fh:
            fh.write(png_elem)
        print(f"Element screenshot saved ({len(png_elem)} bytes) → /tmp/h1.png")
    except Exception as exc:
        print(f"Element screenshot skipped: {exc}")


async def main() -> None:
    print("CDP Browser Control Examples")
    print("=" * 50)
    print(f"Connecting to {CDP_URL}")

    async with CDPConnection(CDP_URL) as conn:
        await demo_navigation(conn)
        await demo_element_selection(conn)
        await demo_text_and_attributes(conn)
        await demo_javascript(conn)
        await demo_screenshot(conn)
        # await demo_interaction(conn)  # Uncomment to test form interaction


if __name__ == "__main__":
    asyncio.run(main())
