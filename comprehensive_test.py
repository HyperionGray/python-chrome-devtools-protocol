#!/usr/bin/env python3

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and report results"""
    print(f"\n=== {description} ===")
    print(f"Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/workspace')
        
        if result.returncode == 0:
            print(f"✓ {description}: PASS")
            if result.stdout:
                print("Output:", result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
        else:
            print(f"✗ {description}: FAIL")
            print("Error:", result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr)
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"✗ {description}: ERROR - {e}")
        return False

def main():
    print("=== Testing PF Tasks (Direct Commands) ===")
    
    # Change to workspace directory
    os.chdir('/workspace')
    
    # Test basic Python functionality
    success_count = 0
    total_tests = 0
    
    # Test 1: Basic import
    total_tests += 1
    if run_command("python3 -c 'import cdp; print(cdp.accessibility)'", "Basic CDP Import"):
        success_count += 1
    
    # Test 2: Generator tests
    total_tests += 1
    if run_command("python3 -m pytest generator/ -v", "Generator Tests"):
        success_count += 1
    
    # Test 3: CDP tests
    total_tests += 1
    if run_command("python3 -m pytest test/ -v", "CDP Tests"):
        success_count += 1
    
    # Test 4: Code generation
    total_tests += 1
    if run_command("python3 generator/generate.py", "Code Generation"):
        success_count += 1
    
    # Test 5: MyPy on generator
    total_tests += 1
    if run_command("python3 -m mypy generator/", "MyPy Generator"):
        success_count += 1
    
    # Test 6: MyPy on CDP
    total_tests += 1
    if run_command("python3 -m mypy cdp/", "MyPy CDP"):
        success_count += 1
    
    print(f"\n=== Test Summary ===")
    print(f"Passed: {success_count}/{total_tests}")
    print(f"Failed: {total_tests - success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("✓ All pf tasks are working correctly!")
    else:
        print("✗ Some pf tasks have issues that need to be addressed.")

if __name__ == "__main__":
    main()