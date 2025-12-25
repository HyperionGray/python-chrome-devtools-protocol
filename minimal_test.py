#!/usr/bin/env python3

# Minimal test to verify basic functionality
import os
import sys

# Change to workspace
os.chdir('/workspace')

print("=== Minimal PF Task Test ===")

# Test 1: Basic import (most fundamental)
print("1. Testing basic CDP import...")
try:
    import cdp
    print("✓ CDP import works")
    
    # Test specific module
    import cdp.accessibility
    print("✓ CDP.accessibility import works")
    
    # This is what the test-import pf task does
    print(f"✓ test-import pf task equivalent: PASS")
    
except Exception as e:
    print(f"✗ Basic import failed: {e}")
    print("✗ test-import pf task equivalent: FAIL")

# Test 2: Check if generator can run
print("\n2. Testing generator...")
try:
    # Check if generator file exists and is runnable
    if os.path.exists('generator/generate.py'):
        print("✓ Generator file exists")
        
        # Try to import the generator module to check syntax
        sys.path.insert(0, 'generator')
        import generate
        print("✓ Generator imports successfully")
        print("✓ generate pf task should work")
    else:
        print("✗ Generator file missing")
        
except Exception as e:
    print(f"✗ Generator test failed: {e}")

# Test 3: Check test files
print("\n3. Testing test structure...")
test_dirs = ['test', 'generator']
for test_dir in test_dirs:
    if os.path.exists(test_dir):
        test_files = [f for f in os.listdir(test_dir) if f.startswith('test_') and f.endswith('.py')]
        print(f"✓ {test_dir}/ has {len(test_files)} test files")
    else:
        print(f"✗ {test_dir}/ directory missing")

print("\n=== Basic Check Complete ===")
print("If basic import works, the core pf tasks should be functional.")