# CDP Connection Module

The `cdp.connection` module provides I/O capabilities for the Chrome DevTools Protocol, including WebSocket management, JSON-RPC message framing, and command multiplexing.

## Installation

Install the library with I/O support:

```bash
pip install chrome-devtools-protocol[io]
```

## Quick Start

```python
import asyncio
from cdp.connection import CDPConnection
from cdp import page, runtime

async def main():
    # Connect using async context manager
    async with CDPConnection("ws://localhost:9222/devtools/page/YOUR_PAGE_ID") as conn:
        # Execute a command
        frame_id, loader_id, error = await conn.execute(
            page.navigate(url="https://example.com")
        )
        
        # Evaluate JavaScript
        result, exception = await conn.execute(
            runtime.evaluate(expression="document.title")
        )
        print(f"Page title: {result.value}")

asyncio.run(main())
```

## Finding the WebSocket URL

To get the WebSocket URL for a Chrome tab:

1. Start Chrome with remote debugging:
   ```bash
   chrome --remote-debugging-port=9222
   ```

2. Open `chrome://inspect/#devices` in Chrome

3. Find your tab and copy the WebSocket URL (looks like `ws://localhost:9222/devtools/page/...`)

## Features

### WebSocket Connection Management

The `CDPConnection` class handles the WebSocket connection lifecycle:

```python
# Manual connection management
conn = CDPConnection(url)
await conn.connect()
# ... use connection ...
await conn.close()

# Or use async context manager (recommended)
async with CDPConnection(url) as conn:
    # ... use connection ...
    pass  # Automatically closed
```

### JSON-RPC Message Framing

The connection automatically:
- Assigns unique IDs to each command
- Tracks pending commands
- Matches responses to their corresponding requests

This is all handled transparently when you call `execute()`.

### Command Multiplexing

Execute multiple commands concurrently:

```python
async with CDPConnection(url) as conn:
    # Start multiple commands at once
    task1 = conn.execute(runtime.evaluate(expression="1 + 1"))
    task2 = conn.execute(runtime.evaluate(expression="2 + 2"))
    task3 = conn.execute(runtime.evaluate(expression="3 + 3"))
    
    # Wait for all to complete
    results = await asyncio.gather(task1, task2, task3)
    
    # Results come back in order, even if responses arrive out of order
    print(results[0][0].value)  # 2
    print(results[1][0].value)  # 4
    print(results[2][0].value)  # 6
```

### Event Handling

Listen for browser events using an async iterator:

```python
async with CDPConnection(url) as conn:
    # Enable events
    await conn.execute(page.enable())
    
    # Listen for events
    async for event in conn.listen():
        if isinstance(event, page.LoadEventFired):
            print(f"Page loaded at {event.timestamp}")
        elif isinstance(event, page.FrameNavigated):
            print(f"Navigated to {event.frame.url}")
```

You can also get events without blocking:

```python
event = conn.get_event_nowait()  # Returns None if no events
if event:
    print(f"Got event: {event}")
```

### Error Handling

The connection module provides typed exceptions:

```python
from cdp.connection import CDPError, CDPConnectionError, CDPCommandError

try:
    async with CDPConnection(url) as conn:
        result = await conn.execute(some_command())
except CDPConnectionError as e:
    print(f"Connection failed: {e}")
except CDPCommandError as e:
    print(f"Command failed: {e.code} - {e.message}")
except asyncio.TimeoutError:
    print("Command timed out")
```

### Timeouts

Set a default timeout for all commands, or override per command:

```python
# Set default timeout to 10 seconds
conn = CDPConnection(url, timeout=10.0)

# Override timeout for specific command
result = await conn.execute(some_command(), timeout=30.0)
```

## API Reference

### CDPConnection

```python
class CDPConnection:
    def __init__(self, url: str, timeout: float = 30.0)
    async def connect(self) -> None
    async def close(self) -> None
    async def execute(self, cmd, timeout: Optional[float] = None) -> Any
    async def listen(self) -> AsyncIterator[Any]
    def get_event_nowait(self) -> Optional[Any]
    
    @property
    def is_connected(self) -> bool
    
    @property
    def pending_command_count(self) -> int
```

### Exceptions

- `CDPError`: Base exception for all CDP errors
- `CDPConnectionError`: Raised when there's a connection problem
- `CDPCommandError`: Raised when a command returns an error
  - `.code`: Error code
  - `.message`: Error message
  - `.data`: Optional additional error data

## Examples

See the [examples directory](../examples/connection_example.py) for complete working examples including:

- Basic navigation and JavaScript evaluation
- Event handling patterns
- Concurrent command execution
- Error handling

## Backward Compatibility

The connection module is completely optional. The core library still works in Sans-I/O mode without the `websockets` dependency. Existing code that uses the Sans-I/O API continues to work unchanged.
