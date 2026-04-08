Browser Control
===============

The ``cdp.browser_control`` module provides a high-level browser automation
API built on top of the raw CDP domain modules and
:class:`~cdp.connection.CDPConnection`.  It offers a set of coroutines
similar to what Playwright or Puppeteer expose, without requiring an external
automation framework.

.. note::

   This module requires the ``websockets`` dependency.  Install it with::

       pip install chrome-devtools-protocol[io]

.. contents::
   :local:
   :depth: 2


Quick Start
-----------

.. code-block:: python

   import asyncio
   from cdp.connection import CDPConnection
   from cdp import browser_control as bc
   from cdp import page

   async def main():
       async with CDPConnection("ws://localhost:9222/devtools/page/ID") as conn:
           # Enable page events (required for wait_for_load)
           await conn.execute(page.enable())

           # Navigate and wait for the page to load
           await bc.navigate(conn, "https://example.com")
           await bc.wait_for_load(conn)

           # Read the heading text
           text = await bc.get_text(conn, "h1")
           print(f"Heading: {text}")

           # Click a link
           await bc.click(conn, "a")

           # Fill a form
           await bc.clear_and_type(conn, "input[name='q']", "hello world")
           await bc.press_key(conn, "Enter")

           # Capture a screenshot
           png_bytes = await bc.screenshot(conn)
           with open("page.png", "wb") as f:
               f.write(png_bytes)

   asyncio.run(main())


Navigation
----------

.. autofunction:: cdp.browser_control.navigate
.. autofunction:: cdp.browser_control.reload
.. autofunction:: cdp.browser_control.go_back
.. autofunction:: cdp.browser_control.go_forward
.. autofunction:: cdp.browser_control.wait_for_load


Element Selection
-----------------

.. autofunction:: cdp.browser_control.query_selector
.. autofunction:: cdp.browser_control.query_selector_all


Element Interaction
-------------------

.. autofunction:: cdp.browser_control.click
.. autofunction:: cdp.browser_control.double_click
.. autofunction:: cdp.browser_control.hover
.. autofunction:: cdp.browser_control.type_text
.. autofunction:: cdp.browser_control.clear_and_type
.. autofunction:: cdp.browser_control.press_key
.. autofunction:: cdp.browser_control.focus
.. autofunction:: cdp.browser_control.select_option


Element Inspection
------------------

.. autofunction:: cdp.browser_control.get_text
.. autofunction:: cdp.browser_control.get_attribute
.. autofunction:: cdp.browser_control.get_bounding_box
.. autofunction:: cdp.browser_control.is_visible


Screenshots
-----------

.. autofunction:: cdp.browser_control.screenshot
.. autofunction:: cdp.browser_control.screenshot_element


JavaScript
----------

.. autofunction:: cdp.browser_control.evaluate
.. autofunction:: cdp.browser_control.evaluate_on_node


Waiting
-------

.. autofunction:: cdp.browser_control.wait_for_selector
.. autofunction:: cdp.browser_control.wait_for_event

``wait_for_selector`` states
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``state`` parameter controls what condition is awaited:

* ``state="attached"`` (default): selector exists in the DOM; returns ``NodeId``.
* ``state="visible"``: selector exists and is visible; returns ``NodeId``.
* ``state="hidden"``: selector is hidden or missing; returns ``None``.
* ``state="detached"``: selector is missing from the DOM; returns ``None``.


Patterns and Recipes
--------------------

Waiting for an element before interacting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   node = await bc.wait_for_selector(conn, "#submit-button", timeout=10)
   await bc.click(conn, node)

Waiting for hidden or detached UI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Wait for a loading spinner to disappear (hidden or removed).
   await bc.wait_for_selector(conn, ".spinner", state="hidden", timeout=10)

   # Wait for a modal to be removed from the DOM.
   await bc.wait_for_selector(conn, "#modal", state="detached", timeout=10)


Checking visibility before clicking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if await bc.is_visible(conn, ".cookie-banner"):
       await bc.click(conn, ".cookie-banner .dismiss")


Reading all list items
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   items = await bc.query_selector_all(conn, "ul.results li")
   for node in items:
       text = await bc.get_text(conn, node)
       print(text)


Extracting a link href
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   href = await bc.get_attribute(conn, "a.download", "href")


Selecting a dropdown value
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   await bc.select_option(conn, "select#country", "US")


Keyboard shortcuts
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Ctrl+A then Delete
   await bc.press_key(conn, "a", modifiers=2)   # Ctrl=2
   await bc.press_key(conn, "Delete")


Capturing a single element screenshot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   png = await bc.screenshot_element(conn, "#logo")
   with open("logo.png", "wb") as f:
       f.write(png)


Running arbitrary JavaScript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   count = await bc.evaluate(conn, "document.querySelectorAll('li').length")
   print(f"Found {count} list items")

   # Operate on a specific element
   checked = await bc.evaluate_on_node(
       conn, "input[type='checkbox']",
       "function() { return this.checked; }"
   )
