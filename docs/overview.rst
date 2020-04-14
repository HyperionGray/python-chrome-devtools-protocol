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

**This library does not perform any I/O!** In order to maximize
flexibility, this library does not actually handle any network I/O, such as
opening a socket or negotiating a WebSocket protocol. Instead, that
responsibility is left to higher-level libraries, for example
`trio-chrome-devtools-protocol
<https://github.com/hyperiongray/trio-chrome-devtools-protocol>`_.

**This package provides Chrome DevTools Protocol r678025.** Download a compatible
Chrome package:

* `Linux <https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/678025/chrome-linux.zip>`_
* `Mac <https://storage.googleapis.com/chromium-browser-snapshots/Mac/678025/chrome-mac.zip>`_
* `Windows 32-bit <https://storage.googleapis.com/chromium-browser-snapshots/Win/678025/chrome-win.zip>`_
* `Windows 64-bit <https://storage.googleapis.com/chromium-browser-snapshots/Win_x64/678025/chrome-win.zip>`_

**Install from PyPI (requires Python ≥3.7):**

::

    $ pip install chrome-devtools-protocol

**Sample code:**

.. code-block:: python

    from cdp import page

    frame_id = page.FrameId('my id')
    assert repr(frame_id) == "FrameId('my id')"
