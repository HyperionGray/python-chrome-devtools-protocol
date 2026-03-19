#!/usr/bin/env python3

import sys
import os
import subprocess

print("=== Quick Environment Check ===")

# Basic Python info
print(f"Python: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Check if we're in the right place
os.chdir('/workspace')
print(f"Workspace files: {sorted(os.listdir('.'))[:10]}")

# Test basic import
print("\n=== Basic Import Test ===")
try:
    import cdp
    print("✓ CDP imports successfully")
    print(f"CDP file: {cdp.__file__}")
    
    # Test a specific module
    import cdp.runtime
    print("✓ CDP.runtime imports successfully")
    
except Exception as e:
    print(f"✗ CDP import failed: {e}")

# Check for pytest
print("\n=== Tool Check ===")
try:
    import pytest
    print(f"✓ pytest available: {pytest.__version__}")
except ImportError:
    print("✗ pytest not available")

try:
    import mypy
    print(f"✓ mypy available")
except ImportError:
    print("✗ mypy not available")

# Test a simple command
print("\n=== Simple Command Test ===")
try:
    result = subprocess.run(['python3', '-c', 'print("Hello from subprocess")'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("✓ Subprocess execution works")
    else:
        print("✗ Subprocess execution failed")
except Exception as e:
    print(f"✗ Subprocess test failed: {e}")

print("\n=== Ready to test PF tasks ===")