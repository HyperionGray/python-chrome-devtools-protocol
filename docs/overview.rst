Overview
========

Python Chrome DevTools Protocol (shortened to PyCDP) is a library that provides
Python wrappers for the types, commands, and events specified in the `Chrome
DevTools Protocol <https://github.com/ChromeDevTools/devtools-protocol/>`_.

The Chrome DevTools Protocol provides for remote control of a web browser by
sending JSON messages over a WebSocket. That JSON format is described by a
machine-readable specification. This specification is used to automatically
generate the classes and methods found in this library.

You could write a CDP client by connecting a WebSocket and then sending JSON
objects, but this would be tedious and error-prone: the Python interpreter would
not catch any typos in your JSON objects, and you wouldn't get autocomplete for
any parts of the JSON data structure. By providing a set of native Python
wrappers, this project makes it easier and faster to write CDP client code.

**Two usage modes are available:**

* **Sans-I/O mode (original):** The core library provides type wrappers without
  performing any I/O. This maximises flexibility and allows integration with any
  async framework such as
  `trio-chrome-devtools-protocol
  <https://github.com/hyperiongray/trio-chrome-devtools-protocol>`_.

* **I/O mode:** The ``cdp.connection`` module handles the WebSocket lifecycle,
  JSON-RPC message framing, and command multiplexing.  The
  ``cdp.browser_control`` module layers a high-level automation API on top of
  this, providing Playwright-style helpers for navigation, element interaction,
  screenshots, and more.  See :doc:`browser_control` for details.

**This package provides Chrome DevTools Protocol r678025.** Download a compatible
Chrome package:

* `Linux <https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/678025/chrome-linux.zip>`_
* `Mac <https://storage.googleapis.com/chromium-browser-snapshots/Mac/678025/chrome-mac.zip>`_
* `Windows 32-bit <https://storage.googleapis.com/chromium-browser-snapshots/Win/678025/chrome-win.zip>`_
* `Windows 64-bit <https://storage.googleapis.com/chromium-browser-snapshots/Win_x64/678025/chrome-win.zip>`_

**Install from PyPI (requires Python ≥3.8):**

::

    $ pip install chrome-devtools-protocol        # Sans-I/O only
    $ pip install chrome-devtools-protocol[io]    # With WebSocket / browser-control support

**Quick example (Sans-I/O mode):**

.. code-block:: python

    from cdp import page

    frame_id = page.FrameId('my id')
    assert repr(frame_id) == "FrameId('my id')"

**Quick example (browser control):**

.. code-block:: python

    import asyncio
    from cdp.connection import CDPConnection
    from cdp import browser_control as bc
    from cdp import page

    async def main():
        async with CDPConnection("ws://localhost:9222/devtools/page/ID") as conn:
            await conn.execute(page.enable())
            await bc.navigate(conn, "https://example.com")
            await bc.wait_for_load(conn)
            print(await bc.get_text(conn, "h1"))

    asyncio.run(main())
