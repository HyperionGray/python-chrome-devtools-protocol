#!/usr/bin/env python3
"""
Example script demonstrating the use of the CDP connection module.

This example shows how to:
1. Connect to a Chrome DevTools Protocol endpoint
2. Execute commands
3. Handle events
4. Multiplex multiple commands concurrently
"""

import asyncio
from cdp.connection import CDPConnection
from cdp import page, runtime


async def basic_example():
    """Basic example: connect, navigate, and get the title."""
    print("=== Basic Example ===")
    
    # Replace with your actual CDP endpoint URL
    # You can get this from chrome://inspect or by starting Chrome with --remote-debugging-port=9222
    url = "ws://localhost:9222/devtools/page/YOUR_PAGE_ID"
    
    async with CDPConnection(url) as conn:
        # Enable page domain events
        await conn.execute(page.enable())
        
        # Navigate to a URL
        frame_id, *_ = await conn.execute(
            page.navigate(url="https://example.com")
        )
        print(f"Navigated to example.com, frame_id: {frame_id}")
        
        # Wait for the next page load event
        load_event = await conn.wait_for(page.LoadEventFired, timeout=5.0)
        print(f"Load event timestamp: {load_event.timestamp}")
        
        # Evaluate some JavaScript
        result, exception = await conn.execute(
            runtime.evaluate(expression="document.title")
        )
        if exception:
            print(f"Error: {exception}")
        else:
            print(f"Page title: {result.value}")


async def event_handling_example():
    """Example showing event handling."""
    print("\n=== Event Handling Example ===")
    
    url = "ws://localhost:9222/devtools/page/YOUR_PAGE_ID"
    
    async with CDPConnection(url) as conn:
        # Enable page domain to receive events
        await conn.execute(page.enable())
        
        # Start navigation
        print("Starting navigation...")
        nav_task = asyncio.create_task(
            conn.execute(page.navigate(url="https://example.com"))
        )
        
        # Wait for a specific event while navigation is in progress
        load_event = await conn.wait_for(page.LoadEventFired, timeout=10.0)
        print(f"Received {type(load_event).__name__} at {load_event.timestamp}")
        
        # Wait for navigation to complete
        await nav_task
        print("Navigation complete!")


async def multiplexing_example():
    """Example showing concurrent command execution (multiplexing)."""
    print("\n=== Multiplexing Example ===")
    
    url = "ws://localhost:9222/devtools/page/YOUR_PAGE_ID"
    
    async with CDPConnection(url) as conn:
        # Execute multiple commands concurrently
        tasks = [
            conn.execute(runtime.evaluate(expression="1 + 1")),
            conn.execute(runtime.evaluate(expression="'hello'.toUpperCase()")),
            conn.execute(runtime.evaluate(expression="Math.PI")),
        ]
        
        # Wait for all commands to complete
        results = await asyncio.gather(*tasks)
        
        # Print results
        for i, (result, exception) in enumerate(results, 1):
            if exception:
                print(f"Command {i} failed: {exception}")
            else:
                print(f"Command {i} result: {result.value}")


async def error_handling_example():
    """Example showing error handling."""
    print("\n=== Error Handling Example ===")
    
    url = "ws://localhost:9222/devtools/page/YOUR_PAGE_ID"
    
    async with CDPConnection(url) as conn:
        try:
            # This will cause a JavaScript error
            result, exception = await conn.execute(
                runtime.evaluate(
                    expression="throw new Error('Test error')",
                    await_promise=False
                )
            )
            
            if exception:
                print(f"JavaScript error (expected): {exception.text}")
            
        except Exception as e:
            print(f"Connection error: {e}")


async def main():
    """Run all examples."""
    print("CDP Connection Examples")
    print("=" * 50)
    print("\nNOTE: These examples require a running Chrome instance")
    print("with remote debugging enabled. Start Chrome with:")
    print("  chrome --remote-debugging-port=9222")
    print("\nThen update the URLs in this script with actual page IDs")
    print("from chrome://inspect/#devices")
    print("=" * 50)
    
    # Uncomment the examples you want to run:
    # await basic_example()
    # await event_handling_example()
    # await multiplexing_example()
    # await error_handling_example()
    
    print("\nTo run these examples, uncomment them in the main() function")


if __name__ == "__main__":
    asyncio.run(main())
