# PyCDP

[![PyPI](https://img.shields.io/pypi/v/chrome-devtools-protocol.svg)](https://pypi.org/project/chrome-devtools-protocol/)
![Python Versions](https://img.shields.io/pypi/pyversions/chrome-devtools-protocol)
![MIT License](https://img.shields.io/github/license/HyperionGray/python-chrome-devtools-protocol.svg)
[![Build Status](https://img.shields.io/travis/com/HyperionGray/python-chrome-devtools-protocol.svg?branch=master)](https://travis-ci.com/HyperionGray/python-chrome-devtools-protocol)
[![Read the Docs](https://img.shields.io/readthedocs/py-cdp.svg)](https://py-cdp.readthedocs.io)

Python Chrome DevTools Protocol (shortened to PyCDP) is a library that provides
Python wrappers for the types, commands, and events specified in the [Chrome
DevTools Protocol](https://github.com/ChromeDevTools/devtools-protocol/).

The Chrome DevTools Protocol provides for remote control of a web browser by
sending JSON messages over a WebSocket. That JSON format is described by a
machine-readable specification. This specification is used to automatically
generate the classes and methods found in this library.

You could write a CDP client by connecting a WebSocket and then sending JSON
objects, but this would be tedious and error-prone: the Python interpreter would
not catch any typos in your JSON objects, and you wouldn't get autocomplete for
any parts of the JSON data structure. By providing a set of native Python
wrappers, this project makes it easier and faster to write CDP client code.

## Two Usage Modes

**Sans-I/O Mode (original):** The core library provides type wrappers without performing any I/O. 
This maximizes flexibility and allows integration with any async framework. This is ideal for users 
who want to integrate CDP with their own I/O stack or use libraries like 
[trio-chrome-devtools-protocol](https://github.com/hyperiongray/trio-chrome-devtools-protocol).

**I/O Mode (new):** The library now includes `cdp.connection` module that provides WebSocket I/O, 
JSON-RPC message framing, and command multiplexing out of the box. This makes it easy to get started 
with CDP without writing any I/O code yourself.

## Installation

**Basic installation (Sans-I/O mode only):**

```bash
pip install chrome-devtools-protocol
```

**With I/O support:**

```bash
pip install chrome-devtools-protocol[io]
```

## Quick Start with I/O Mode

```python
import asyncio
from cdp.connection import CDPConnection
from cdp import page

async def main():
    # Connect to a Chrome DevTools Protocol endpoint
    async with CDPConnection("ws://localhost:9222/devtools/page/YOUR_PAGE_ID") as conn:
        # Navigate to a URL
        frame_id, loader_id, error = await conn.execute(
            page.navigate(url="https://example.com")
        )
        print(f"Navigated to example.com, frame_id: {frame_id}")

asyncio.run(main())
```

### Key Features of I/O Mode

- **WebSocket Management**: Automatic connection lifecycle management with async context managers
- **JSON-RPC Framing**: Automatic message ID assignment and request/response matching
- **Command Multiplexing**: Execute multiple commands concurrently with proper tracking
- **Event Handling**: Async iterator for receiving browser events
- **Error Handling**: Comprehensive error handling with typed exceptions

See the [examples directory](examples/) for more usage patterns.

## Sans-I/O Mode (Original)

For users who prefer to manage their own I/O:

```python
from cdp import page

frame_id = page.FrameId('my id')
assert repr(frame_id) == "FrameId('my id')"
```

## API Reference

PyCDP provides Python wrappers for all Chrome DevTools Protocol domains. Here are some commonly used domains:

### Core Domains
- **`cdp.page`** - Page navigation, lifecycle, and screenshot capabilities
- **`cdp.network`** - Network request/response monitoring and modification
- **`cdp.runtime`** - JavaScript runtime interaction and evaluation
- **`cdp.dom`** - DOM tree inspection and manipulation
- **`cdp.debugger`** - JavaScript debugging capabilities

### Browser Control
- **`cdp.browser`** - Browser-level operations and window management
- **`cdp.target`** - Target (tab/page) creation and management
- **`cdp.emulation`** - Device emulation and viewport control
- **`cdp.input_`** - Input event simulation (mouse, keyboard, touch)

### Monitoring & Analysis
- **`cdp.performance`** - Performance metrics and profiling
- **`cdp.console`** - Console message handling
- **`cdp.log`** - Log entry handling
- **`cdp.tracing`** - Chrome tracing for performance analysis

### Storage & Security
- **`cdp.storage`** - Storage management (cookies, cache, IndexedDB, Privacy Sandbox)
- **`cdp.security`** - Security state and certificate information
- **`cdp.audits`** - Automated security and privacy issue detection
- **`cdp.fetch`** - Network request interception and modification

### Advanced Features
- **`cdp.extensions`** - Browser extension management and testing
- **`cdp.fed_cm`** - Federated Credential Management (FedCM) testing
- **`cdp.device_access`** - Device permission prompt handling
- **`cdp.web_authn`** - WebAuthn virtual authenticator support

For complete API documentation, see the [full documentation](https://py-cdp.readthedocs.io).

## Examples

Check the [examples directory](examples/) for practical usage examples.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

For security-related matters, please see [SECURITY.md](SECURITY.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and migration guides.

## Documentation

For more information, see the [complete documentation](https://py-cdp.readthedocs.io).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<a href="https://www.hyperiongray.com/?pk_campaign=github&pk_kwd=pycdp"><img alt="define hyperion gray" width="500px" src="https://hyperiongray.s3.amazonaws.com/define-hg.svg"></a>
