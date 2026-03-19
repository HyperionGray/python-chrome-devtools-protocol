#!/bin/bash

echo "=== Environment Check ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python3 --version 2>&1)"
echo "Pip version: $(pip3 --version 2>&1)"

echo -e "\n=== Checking for required tools ==="
echo "Poetry: $(which poetry 2>/dev/null || echo 'Not found')"
echo "Make: $(which make 2>/dev/null || echo 'Not found')"
echo "MyPy: $(which mypy 2>/dev/null || echo 'Not found')"
echo "Pytest: $(which pytest 2>/dev/null || echo 'Not found')"

echo -e "\n=== Python modules check ==="
python3 -c "
import sys
modules = ['pytest', 'mypy', 'inflection']
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module} available')
    except ImportError:
        print(f'✗ {module} not available')
"

echo -e "\n=== Basic CDP import test ==="
cd /workspace
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    import cdp
    print('✓ CDP module imports successfully')
    print(f'CDP location: {cdp.__file__}')
except Exception as e:
    print(f'✗ CDP import failed: {e}')
"