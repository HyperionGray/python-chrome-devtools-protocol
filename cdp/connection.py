"""
CDP Connection Module

This module provides I/O and multiplexing support for Chrome DevTools Protocol.
It handles WebSocket connections, JSON-RPC message framing, command multiplexing,
and event dispatching.
"""

from __future__ import annotations
import asyncio
import json
import logging
import typing
from dataclasses import dataclass, field

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    WebSocketClientProtocol = typing.Any  # type: ignore

from cdp.util import parse_json_event, T_JSON_DICT


logger = logging.getLogger(__name__)


class CDPError(Exception):
    """Base exception for CDP errors."""
    pass


class CDPConnectionError(CDPError):
    """Raised when there's a connection error."""
    pass


class CDPCommandError(CDPError):
    """Raised when a command returns an error."""
    
    def __init__(self, code: int, message: str, data: typing.Optional[typing.Any] = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"CDP Command Error {code}: {message}")


@dataclass
class PendingCommand:
    """Represents a command waiting for a response."""
    future: asyncio.Future
    method: str
    params: T_JSON_DICT


class CDPConnection:
    """
    Manages a WebSocket connection to Chrome DevTools Protocol.
    
    This class handles:
    - WebSocket connection management
    - JSON-RPC message framing (request ID assignment)
    - Command multiplexing (tracking multiple concurrent commands)
    - Event dispatching
    - Error handling
    
    Example:
        async with CDPConnection("ws://localhost:9222/devtools/page/...") as conn:
            # Send a command
            result = await conn.execute(some_command())
            
            # Listen for events
            async for event in conn.listen():
                print(event)
    """
    
    def __init__(self, url: str, timeout: float = 30.0):
        """
        Initialize a CDP connection.
        
        Args:
            url: WebSocket URL for the CDP endpoint
            timeout: Default timeout for commands in seconds
        """
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError(
                "websockets library is required for CDPConnection. "
                "Install it with: pip install websockets"
            )
        
        self.url = url
        self.timeout = timeout
        self._ws: typing.Optional[WebSocketClientProtocol] = None
        self._next_command_id = 1
        self._pending_commands: typing.Dict[int, PendingCommand] = {}
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._recv_task: typing.Optional[asyncio.Task] = None
        self._closed = False
    
    async def connect(self) -> None:
        """Establish the WebSocket connection."""
        if self._ws is not None:
            raise CDPConnectionError("Already connected")
        
        try:
            self._ws = await websockets.connect(self.url)  # type: ignore
            self._recv_task = asyncio.create_task(self._receive_loop())
            logger.info(f"Connected to {self.url}")
        except Exception as e:
            raise CDPConnectionError(f"Failed to connect to {self.url}: {e}")
    
    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self._closed:
            return
        
        self._closed = True
        
        # Cancel the receive task
        if self._recv_task:
            self._recv_task.cancel()
            try:
                await self._recv_task
            except asyncio.CancelledError:
                pass
        
        # Cancel all pending commands
        for cmd_id, pending in self._pending_commands.items():
            if not pending.future.done():
                pending.future.cancel()
        self._pending_commands.clear()
        
        # Close the WebSocket
        if self._ws:
            await self._ws.close()
            self._ws = None
        
        logger.info("Connection closed")
    
    async def __aenter__(self) -> CDPConnection:
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
    
    async def _receive_loop(self) -> None:
        """
        Main receive loop that processes incoming WebSocket messages.
        
        This loop:
        - Receives messages from the WebSocket
        - Parses JSON-RPC responses and matches them to pending commands
        - Dispatches events to the event queue
        """
        try:
            while not self._closed and self._ws:
                try:
                    message = await self._ws.recv()
                    data = json.loads(message)
                    
                    if 'id' in data:
                        # This is a command response
                        await self._handle_response(data)
                    elif 'method' in data:
                        # This is an event
                        await self._handle_event(data)
                    else:
                        logger.warning(f"Received unexpected message: {data}")
                
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON: {e}")
                except Exception as e:
                    logger.error(f"Error in receive loop: {e}")
                    if not self._closed:
                        raise
        except asyncio.CancelledError:
            logger.debug("Receive loop cancelled")
        except Exception as e:
            logger.error(f"Fatal error in receive loop: {e}")
            # Cancel all pending commands with this error
            for pending in self._pending_commands.values():
                if not pending.future.done():
                    pending.future.set_exception(CDPConnectionError(f"Connection error: {e}"))
    
    async def _handle_response(self, data: T_JSON_DICT) -> None:
        """Handle a command response."""
        cmd_id = data['id']
        
        if cmd_id not in self._pending_commands:
            logger.warning(f"Received response for unknown command ID {cmd_id}")
            return
        
        pending = self._pending_commands.pop(cmd_id)
        
        if 'error' in data:
            error = data['error']
            exc = CDPCommandError(
                code=error.get('code', -1),
                message=error.get('message', 'Unknown error'),
                data=error.get('data')
            )
            pending.future.set_exception(exc)
        else:
            result = data.get('result', {})
            pending.future.set_result(result)
    
    async def _handle_event(self, data: T_JSON_DICT) -> None:
        """Handle an event notification."""
        try:
            event = parse_json_event(data)
            await self._event_queue.put(event)
        except Exception as e:
            logger.error(f"Failed to parse event: {e}")
    
    async def execute(
        self,
        cmd: typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Any],
        timeout: typing.Optional[float] = None
    ) -> typing.Any:
        """
        Execute a CDP command.
        
        This method:
        - Assigns a unique ID to the command
        - Sends it over the WebSocket
        - Waits for the response (with multiplexing support)
        - Returns the parsed result
        
        Args:
            cmd: A CDP command generator (from any CDP domain module)
            timeout: Optional timeout override for this command
        
        Returns:
            The command result (type depends on the command)
        
        Raises:
            CDPCommandError: If the command returns an error
            asyncio.TimeoutError: If the command times out
            CDPConnectionError: If there's a connection error
        
        Example:
            from cdp import page
            result = await conn.execute(page.navigate(url="https://example.com"))
        """
        if self._ws is None:
            raise CDPConnectionError("Not connected")
        
        if self._closed:
            raise CDPConnectionError("Connection closed")
        
        # Get the command request from the generator
        request = cmd.send(None)  # type: ignore[arg-type]
        
        # Assign a unique ID
        cmd_id = self._next_command_id
        self._next_command_id += 1
        request['id'] = cmd_id
        
        # Create a future to track this command
        future: asyncio.Future = asyncio.Future()
        self._pending_commands[cmd_id] = PendingCommand(
            future=future,
            method=request['method'],
            params=request.get('params', {})
        )
        
        try:
            # Send the command
            await self._ws.send(json.dumps(request))
            logger.debug(f"Sent command {cmd_id}: {request['method']}")
            
            # Wait for the response
            timeout_val = timeout if timeout is not None else self.timeout
            result = await asyncio.wait_for(future, timeout=timeout_val)
            
            # Send the result back to the generator
            try:
                cmd.send(result)
            except StopIteration as e:
                return e.value
            
            raise CDPError("Command generator did not stop")
            
        except asyncio.TimeoutError:
            # Clean up the pending command
            self._pending_commands.pop(cmd_id, None)
            raise asyncio.TimeoutError(f"Command {request['method']} timed out")
        except Exception:
            # Clean up the pending command on error
            self._pending_commands.pop(cmd_id, None)
            raise
    
    async def listen(self) -> typing.AsyncIterator[typing.Any]:
        """
        Listen for events from the browser.
        
        This is an async iterator that yields CDP events as they arrive.
        
        Yields:
            CDP event objects (type depends on the event)
        
        Example:
            async for event in conn.listen():
                if isinstance(event, page.LoadEventFired):
                    print("Page loaded!")
        """
        while not self._closed:
            try:
                event = await asyncio.wait_for(self._event_queue.get(), timeout=1.0)
                yield event
            except asyncio.TimeoutError:
                # Check if connection is still alive
                if self._closed:
                    break
                continue
    
    def get_event_nowait(self) -> typing.Optional[typing.Any]:
        """
        Get an event from the queue without waiting.
        
        Returns:
            A CDP event object, or None if no events are available
        """
        try:
            return self._event_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None
    
    @property
    def is_connected(self) -> bool:
        """Check if the connection is open."""
        return self._ws is not None and not self._closed
    
    @property
    def pending_command_count(self) -> int:
        """Get the number of pending commands (for debugging/monitoring)."""
        return len(self._pending_commands)
