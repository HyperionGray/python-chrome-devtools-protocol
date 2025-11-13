"""
Tests for the cdp.connection module.
"""
import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from cdp.connection import (
    CDPConnection, CDPError, CDPConnectionError, CDPCommandError,
    PendingCommand
)
from cdp import page, runtime


# Mock WebSocket for testing
class MockWebSocket:
    """Mock WebSocket for testing."""
    
    def __init__(self):
        self.sent_messages = []
        self.messages_to_receive = []
        self.closed = False
    
    async def send(self, message):
        """Mock send method."""
        if self.closed:
            raise RuntimeError("WebSocket is closed")
        self.sent_messages.append(message)
    
    async def recv(self):
        """Mock recv method."""
        if self.closed:
            raise RuntimeError("WebSocket is closed")
        # Wait for messages to become available
        while not self.messages_to_receive and not self.closed:
            await asyncio.sleep(0.01)
        if self.closed:
            raise RuntimeError("WebSocket is closed")
        return self.messages_to_receive.pop(0)
    
    async def close(self):
        """Mock close method."""
        self.closed = True
    
    def queue_message(self, message):
        """Queue a message to be received."""
        if isinstance(message, dict):
            message = json.dumps(message)
        self.messages_to_receive.append(message)


@pytest.mark.asyncio
async def test_connection_lifecycle():
    """Test basic connection lifecycle."""
    mock_ws = MockWebSocket()
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        conn = CDPConnection("ws://localhost:9222/test")
        assert not conn.is_connected
        
        await conn.connect()
        assert conn.is_connected
        assert mock_connect.called
        
        await conn.close()
        assert not conn.is_connected
        assert mock_ws.closed


@pytest.mark.asyncio
async def test_context_manager():
    """Test async context manager."""
    mock_ws = MockWebSocket()
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        async with CDPConnection("ws://localhost:9222/test") as conn:
            assert conn.is_connected
        
        assert not conn.is_connected
        assert mock_ws.closed


@pytest.mark.asyncio
async def test_execute_command_success():
    """Test executing a command successfully."""
    mock_ws = MockWebSocket()
    
    # Queue a successful response
    response = {
        "id": 1,
        "result": {
            "frameId": "test-frame-id"
        }
    }
    mock_ws.queue_message(response)
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        async with CDPConnection("ws://localhost:9222/test") as conn:
            # Execute a command
            result = await conn.execute(page.navigate(url="https://example.com"))
            
            # Check that the command was sent
            assert len(mock_ws.sent_messages) == 1
            sent = json.loads(mock_ws.sent_messages[0])
            assert sent['id'] == 1
            assert sent['method'] == 'Page.navigate'
            assert sent['params']['url'] == 'https://example.com'
            
            # Check the result (navigate returns a tuple)
            assert isinstance(result, tuple)
            assert len(result) == 4
            frame_id, loader_id, error_text, is_download = result
            assert isinstance(frame_id, page.FrameId)
            assert frame_id == page.FrameId('test-frame-id')


@pytest.mark.asyncio
async def test_execute_command_error():
    """Test executing a command that returns an error."""
    mock_ws = MockWebSocket()
    
    # Queue an error response
    response = {
        "id": 1,
        "error": {
            "code": -32602,
            "message": "Invalid params"
        }
    }
    mock_ws.queue_message(response)
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        async with CDPConnection("ws://localhost:9222/test") as conn:
            # Execute a command that will fail
            with pytest.raises(CDPCommandError) as exc_info:
                await conn.execute(page.navigate(url="https://example.com"))
            
            assert exc_info.value.code == -32602
            assert "Invalid params" in str(exc_info.value)


@pytest.mark.asyncio
async def test_execute_multiple_commands_multiplexing():
    """Test executing multiple commands concurrently (multiplexing)."""
    mock_ws = MockWebSocket()
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        async with CDPConnection("ws://localhost:9222/test") as conn:
            # Start three commands concurrently
            task1 = asyncio.create_task(
                conn.execute(page.navigate(url="https://example1.com"))
            )
            # Wait a bit to ensure command 1 is sent
            await asyncio.sleep(0.05)
            
            task2 = asyncio.create_task(
                conn.execute(runtime.evaluate(expression="'Hello'"))
            )
            await asyncio.sleep(0.05)
            
            task3 = asyncio.create_task(
                conn.execute(runtime.evaluate(expression="42"))
            )
            await asyncio.sleep(0.05)
            
            # Queue responses in different order than requests
            response2 = {
                "id": 2,
                "result": {"result": {"type": "string", "value": "Hello"}}
            }
            response1 = {
                "id": 1,
                "result": {"frameId": "frame-1"}
            }
            response3 = {
                "id": 3,
                "result": {"result": {"type": "number", "value": 42}}
            }
            mock_ws.queue_message(response2)
            mock_ws.queue_message(response1)
            mock_ws.queue_message(response3)
            
            # Wait for all to complete
            results = await asyncio.gather(task1, task2, task3)
            
            # Verify results
            assert isinstance(results[0], tuple)  # navigate returns a tuple
            assert isinstance(results[0][0], page.FrameId)
            assert results[0][0] == page.FrameId('frame-1')
            
            # evaluate returns a tuple (RemoteObject, Optional[ExceptionDetails])
            assert isinstance(results[1], tuple)
            assert isinstance(results[1][0], runtime.RemoteObject)
            assert results[1][0].value == "Hello"
            
            assert isinstance(results[2], tuple)
            assert isinstance(results[2][0], runtime.RemoteObject)
            assert results[2][0].value == 42
            
            # Verify that all three commands were sent
            assert len(mock_ws.sent_messages) == 3


@pytest.mark.asyncio
async def test_command_timeout():
    """Test command timeout."""
    mock_ws = MockWebSocket()
    # Don't queue any response - command will timeout
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        async with CDPConnection("ws://localhost:9222/test", timeout=0.1) as conn:
            # Execute a command that will timeout
            with pytest.raises(asyncio.TimeoutError):
                await conn.execute(page.navigate(url="https://example.com"))


@pytest.mark.asyncio
async def test_event_handling():
    """Test receiving and parsing events."""
    mock_ws = MockWebSocket()
    
    # Queue an event
    event = {
        "method": "Page.loadEventFired",
        "params": {
            "timestamp": 123456.789
        }
    }
    mock_ws.queue_message(event)
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        async with CDPConnection("ws://localhost:9222/test") as conn:
            # Listen for the event
            async def get_event():
                async for evt in conn.listen():
                    return evt
            
            # Get the event with timeout
            received_event = await asyncio.wait_for(get_event(), timeout=1.0)
            
            # Verify the event
            assert isinstance(received_event, page.LoadEventFired)
            assert received_event.timestamp == 123456.789


@pytest.mark.asyncio
async def test_get_event_nowait():
    """Test getting events without waiting."""
    mock_ws = MockWebSocket()
    
    # Queue an event
    event = {
        "method": "Page.loadEventFired",
        "params": {
            "timestamp": 123456.789
        }
    }
    mock_ws.queue_message(event)
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        async with CDPConnection("ws://localhost:9222/test") as conn:
            # Initially no events
            assert conn.get_event_nowait() is None
            
            # Wait a bit for the event to be processed
            await asyncio.sleep(0.1)
            
            # Now we should have an event
            received_event = conn.get_event_nowait()
            assert received_event is not None
            assert isinstance(received_event, page.LoadEventFired)


@pytest.mark.asyncio
async def test_pending_command_count():
    """Test tracking pending command count."""
    mock_ws = MockWebSocket()
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        async with CDPConnection("ws://localhost:9222/test") as conn:
            assert conn.pending_command_count == 0
            
            # Start a command without responding (it will timeout)
            task = asyncio.create_task(
                conn.execute(page.navigate(url="https://example.com"), timeout=10.0)
            )
            
            # Give it time to send the command
            await asyncio.sleep(0.1)
            assert conn.pending_command_count == 1
            
            # Respond to the command
            response = {
                "id": 1,
                "result": {"frameId": "test-frame-id"}
            }
            mock_ws.queue_message(response)
            
            # Wait for the command to complete
            await task
            
            await asyncio.sleep(0.1)
            assert conn.pending_command_count == 0


@pytest.mark.asyncio
async def test_connection_error_handling():
    """Test handling connection errors."""
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.side_effect = Exception("Connection failed")
        
        conn = CDPConnection("ws://localhost:9222/test")
        
        with pytest.raises(CDPConnectionError):
            await conn.connect()


@pytest.mark.asyncio
async def test_close_cancels_pending_commands():
    """Test that closing the connection cancels pending commands."""
    mock_ws = MockWebSocket()
    # Don't queue any response
    
    with patch('cdp.connection.websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        
        conn = CDPConnection("ws://localhost:9222/test", timeout=10.0)
        await conn.connect()
        
        # Start a command that won't get a response
        task = asyncio.create_task(
            conn.execute(page.navigate(url="https://example.com"))
        )
        
        # Give it time to send
        await asyncio.sleep(0.1)
        assert conn.pending_command_count == 1
        
        # Close the connection
        await conn.close()
        
        # The command should be cancelled
        with pytest.raises(asyncio.CancelledError):
            await task


def test_import_without_websockets():
    """Test that the module can be imported without websockets."""
    # This test verifies that importing the module doesn't fail
    # even if websockets is not available (it's checked at runtime)
    from cdp import connection
    assert connection.CDPConnection is not None
    assert connection.CDPError is not None


def test_connection_without_websockets_raises_error():
    """Test that creating a connection without websockets raises an error."""
    with patch('cdp.connection.WEBSOCKETS_AVAILABLE', False):
        with pytest.raises(ImportError, match="websockets library is required"):
            CDPConnection("ws://localhost:9222/test")
