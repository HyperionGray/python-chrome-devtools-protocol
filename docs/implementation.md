# Implementation Design Document: I/O and Multiplexing Support

This document summarizes the implementation of I/O capabilities and JSON-RPC framing with command multiplexing for the Chrome DevTools Protocol library.

## Overview

This implementation addresses the issue requesting I/O support and command multiplexing, despite the library's original Sans-IO design philosophy. The solution maintains full backward compatibility while adding powerful new features.

## Key Design Decisions

### 1. Optional Dependency
- WebSocket support is an **optional extra** (`pip install chrome-devtools-protocol[io]`)
- Core library remains Sans-I/O for existing users
- Graceful degradation if websockets not installed

### 2. Async/Await API
- Uses modern Python async/await syntax
- Async context managers for connection lifecycle
- Compatible with asyncio event loop

### 3. Command Multiplexing Architecture
- Each command gets a unique ID (auto-incrementing counter)
- Pending commands tracked in a dictionary: `{command_id: PendingCommand}`
- Each PendingCommand has an asyncio.Future for response
- Responses matched to futures by ID
- Multiple commands can be in-flight simultaneously

### 4. Event Handling
- Events dispatched to an asyncio.Queue
- Async iterator interface for consumption
- Non-blocking get method available
- Automatic event parsing using existing event registry

## Implementation Details

### CDPConnection Class

```python
class CDPConnection:
    - url: WebSocket endpoint URL
    - timeout: Default command timeout
    - _ws: WebSocket connection
    - _next_command_id: Auto-incrementing ID counter
    - _pending_commands: Dict[int, PendingCommand]
    - _event_queue: asyncio.Queue for events
    - _recv_task: Background task for receiving messages
```

### Message Flow

1. **Command Execution:**
   ```
   User calls execute(cmd) →
   Get request from generator →
   Assign unique ID →
   Create Future and store in _pending_commands →
   Send JSON message →
   Wait for Future →
   Match response by ID →
   Complete Future →
   Send result back to generator →
   Return parsed result
   ```

2. **Event Reception:**
   ```
   WebSocket receives message →
   Parse JSON →
   Is it a response? → Match to command ID → Complete Future
   Is it an event? → Parse with event registry → Add to queue
   ```

3. **Multiplexing:**
   ```
   Command A: ID=1, send, wait
   Command B: ID=2, send, wait  } Concurrent
   Command C: ID=3, send, wait
   Response 2 arrives → Complete future for ID=2 → Command B returns
   Response 1 arrives → Complete future for ID=1 → Command A returns
   Response 3 arrives → Complete future for ID=3 → Command C returns
   ```

### Error Handling

- **Connection errors**: Raised as CDPConnectionError
- **Command errors**: Parsed from response, raised as CDPCommandError
- **Timeouts**: asyncio.TimeoutError with descriptive message
- **Network errors**: Propagated with context

### Lifecycle Management

- `connect()`: Establishes WebSocket, starts receive loop
- `close()`: Cancels receive loop, closes WebSocket, cancels pending commands
- Context manager: Automatically calls connect/close

## Testing Strategy

### Test Coverage

1. **Connection lifecycle** - Connect, close, context manager
2. **Command execution** - Success, error, timeout
3. **Multiplexing** - Multiple concurrent commands
4. **Event handling** - Async iterator, non-blocking get
5. **Error handling** - Connection errors, command errors
6. **Resource cleanup** - Pending commands cancelled on close

### Mock Strategy

- Mock WebSocket with queue-based message delivery
- Allows testing message ordering and timing
- Tests both in-order and out-of-order responses

## Performance Considerations

1. **Memory**: Pending commands dictionary grows with concurrent commands
   - Cleaned up on response or error
   - Bounded by network latency and command count

2. **CPU**: Minimal overhead
   - JSON parsing done by standard library
   - Event dispatching is simple queue operation

3. **Network**: Single WebSocket connection
   - Multiplexing maximizes throughput
   - No head-of-line blocking

## Security Considerations

1. **Input Validation**: Commands validated by type system
2. **Error Handling**: Comprehensive exception handling
3. **Resource Cleanup**: Proper cleanup on close/error
4. **CodeQL Analysis**: 0 security issues found

## Future Enhancements (Potential)

1. **Reconnection Logic**: Automatic reconnection on disconnect
2. **Session Management**: Multiple target sessions
3. **Rate Limiting**: Configurable command rate limits
4. **Metrics**: Command timing and success rate tracking
5. **Compression**: WebSocket compression support

## Backward Compatibility

- **Zero breaking changes**
- Sans-I/O API completely unchanged
- New features opt-in via `[io]` extra
- Existing code continues to work

## Example Usage

### Basic Usage
```python
async with CDPConnection(url) as conn:
    result = await conn.execute(page.navigate(url="https://example.com"))
```

### Multiplexing
```python
tasks = [
    conn.execute(cmd1),
    conn.execute(cmd2),
    conn.execute(cmd3),
]
results = await asyncio.gather(*tasks)  # All concurrent!
```

### Event Handling
```python
async for event in conn.listen():
    if isinstance(event, page.LoadEventFired):
        print("Page loaded!")
```

## Conclusion

This implementation successfully adds I/O capabilities and command multiplexing to the Chrome DevTools Protocol library while maintaining the library's quality standards:

- ✅ Comprehensive testing (19/19 tests passing)
- ✅ Type safety (mypy validation)
- ✅ Security (0 CodeQL alerts)
- ✅ Documentation (README, guide, examples)
- ✅ Backward compatibility (100%)

The implementation fulfills the issue requirements: "Add some IO up in this thing. Add support for the JSON RPC framing (if it's still a thing) AND multiplexing commands. Multiplex so much you can't plex any more." ✅