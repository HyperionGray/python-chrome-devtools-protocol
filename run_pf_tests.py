#!/usr/bin/env python3

# Quick test to see if basic functionality works before comprehensive testing
import os
import sys
import subprocess

os.chdir('/workspace')

print("=== Pre-Test Check ===")

# 1. Check basic import
print("1. Basic import test:")
try:
    import cdp
    print("✓ CDP imports")
except Exception as e:
    print(f"✗ CDP import failed: {e}")

# 2. Check if we can run python commands
print("\n2. Subprocess test:")
try:
    result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
    print(f"✓ Python subprocess works: {result.stdout.strip()}")
except Exception as e:
    print(f"✗ Subprocess failed: {e}")

# 3. Check key files exist
print("\n3. File structure check:")
key_files = ['.pf', 'generator/generate.py', 'test/', 'cdp/']
for file_path in key_files:
    if os.path.exists(file_path):
        print(f"✓ {file_path} exists")
    else:
        print(f"✗ {file_path} missing")

# 4. Try one simple command from pf file
print("\n4. Simple pf command test:")
try:
    # This is the test-import command from .pf file
    result = subprocess.run(
        "python3 -c 'import cdp; print(cdp.accessibility)'", 
        shell=True, 
        capture_output=True, 
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        print("✓ test-import equivalent works")
        print(f"Output: {result.stdout.strip()}")
    else:
        print(f"✗ test-import equivalent failed: {result.stderr}")
except Exception as e:
    print(f"✗ Simple command test failed: {e}")

print("\n=== Pre-Test Complete ===")
print("If basic tests pass, proceeding with comprehensive pf testing...")

# Now run the comprehensive test
print("\n" + "="*60)
print("STARTING COMPREHENSIVE PF TASK TESTING")
print("="*60)

# Import and run the comprehensive test
exec(open('test_every_pf_command.py').read())