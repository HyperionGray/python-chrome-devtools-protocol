#!/bin/bash

# Test each pf task systematically
echo "=== PF Task Testing ==="
echo "Testing each task defined in .pf file"
echo

cd /workspace

# Test 1: Basic import (test-import equivalent)
echo "1. Testing basic import (test-import task):"
if python3 -c 'import cdp; print("✓ CDP import works:", cdp.accessibility)'; then
    echo "✓ test-import task: PASS"
else
    echo "✗ test-import task: FAIL"
fi
echo

# Test 2: Generator tests
echo "2. Testing generator (test-generate task):"
if python3 -m pytest generator/ -v; then
    echo "✓ test-generate task: PASS"
else
    echo "✗ test-generate task: FAIL"
fi
echo

# Test 3: CDP tests  
echo "3. Testing CDP modules (test-cdp task):"
if python3 -m pytest test/ -v; then
    echo "✓ test-cdp task: PASS"
else
    echo "✗ test-cdp task: FAIL"
fi
echo

# Test 4: Code generation
echo "4. Testing code generation (generate task):"
if python3 generator/generate.py; then
    echo "✓ generate task: PASS"
else
    echo "✗ generate task: FAIL"
fi
echo

# Test 5: Type checking generator
echo "5. Testing mypy on generator (mypy-generate):"
if python3 -m mypy generator/; then
    echo "✓ mypy-generate task: PASS"
else
    echo "✗ mypy-generate task: FAIL"
fi
echo

# Test 6: Type checking CDP
echo "6. Testing mypy on CDP (mypy-cdp):"
if python3 -m mypy cdp/; then
    echo "✓ mypy-cdp task: PASS"
else
    echo "✗ mypy-cdp task: FAIL"
fi
echo

echo "=== PF Task Testing Complete ==="