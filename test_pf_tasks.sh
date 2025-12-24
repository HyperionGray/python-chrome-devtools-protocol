#!/bin/bash

# Test script for all pf tasks in .pf file
# This tests every command to ensure they work correctly

echo "=== Testing PF Tasks ==="
echo "Testing all commands from .pf file..."
echo

# Check if poetry is available
if ! command -v poetry &> /dev/null; then
    echo "ERROR: Poetry not found. Cannot test pf tasks."
    exit 1
fi

echo "Poetry found: $(poetry --version)"
echo

# Test basic import first
echo "=== Testing basic import ==="
if poetry run python -c 'import cdp; print("CDP import successful")'; then
    echo "✓ Basic CDP import works"
else
    echo "✗ Basic CDP import failed"
fi
echo

# Test individual make targets that pf tasks wrap
echo "=== Testing individual Makefile targets ==="

echo "Testing: make test-import"
if poetry run make test-import; then
    echo "✓ test-import task works"
else
    echo "✗ test-import task failed"
fi
echo

echo "Testing: make generate"
if poetry run make generate; then
    echo "✓ generate task works"
else
    echo "✗ generate task failed"
fi
echo

echo "Testing: make mypy-generate"
if poetry run make mypy-generate; then
    echo "✓ mypy-generate task works"
else
    echo "✗ mypy-generate task failed"
fi
echo

echo "Testing: make mypy-cdp"
if poetry run make mypy-cdp; then
    echo "✓ mypy-cdp task works"
else
    echo "✗ mypy-cdp task failed"
fi
echo

echo "Testing: make test-generate"
if poetry run make test-generate; then
    echo "✓ test-generate task works"
else
    echo "✗ test-generate task failed"
fi
echo

echo "Testing: make test-cdp"
if poetry run make test-cdp; then
    echo "✓ test-cdp task works"
else
    echo "✗ test-cdp task failed"
fi
echo

echo "Testing: make docs"
if poetry run make docs; then
    echo "✓ docs task works"
else
    echo "✗ docs task failed"
fi
echo

echo "Testing: make default (full pipeline)"
if poetry run make default; then
    echo "✓ default task works"
else
    echo "✗ default task failed"
fi
echo

echo "=== PF Task Testing Complete ==="
echo "All underlying commands for pf tasks have been tested."