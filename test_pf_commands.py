#!/usr/bin/env python3

# Direct test of pf task commands without external dependencies
import os
import sys
import subprocess

def test_command(cmd, name, timeout=30):
    """Test a command and return success/failure"""
    print(f"\n--- Testing {name} ---")
    print(f"Command: {cmd}")
    
    try:
        # Change to workspace directory
        os.chdir('/workspace')
        
        # Run the command
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            print(f"✓ {name}: SUCCESS")
            # Show first few lines of output
            if result.stdout:
                lines = result.stdout.split('\n')[:3]
                print(f"Output preview: {' | '.join(lines)}")
            return True
        else:
            print(f"✗ {name}: FAILED (exit code: {result.returncode})")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {name}: TIMEOUT")
        return False
    except Exception as e:
        print(f"✗ {name}: ERROR - {e}")
        return False

def main():
    print("=== Testing All PF Tasks ===")
    print("Testing the underlying commands for each pf task")
    
    # Test results tracking
    results = {}
    
    # Test each pf task's underlying command
    # Note: Testing without poetry first to see what works
    
    # 1. Test basic import (test-import task)
    results['test-import'] = test_command(
        "python3 -c 'import cdp; print(cdp.accessibility)'",
        "test-import"
    )
    
    # 2. Test code generation (generate task)
    results['generate'] = test_command(
        "python3 generator/generate.py",
        "generate"
    )
    
    # 3. Test generator tests (test-generate task)
    results['test-generate'] = test_command(
        "python3 -m pytest generator/ -v",
        "test-generate"
    )
    
    # 4. Test CDP tests (test-cdp task)
    results['test-cdp'] = test_command(
        "python3 -m pytest test/ -v",
        "test-cdp"
    )
    
    # 5. Test mypy on generator (mypy-generate)
    results['mypy-generate'] = test_command(
        "python3 -m mypy generator/",
        "mypy-generate"
    )
    
    # 6. Test mypy on CDP (mypy-cdp)
    results['mypy-cdp'] = test_command(
        "python3 -m mypy cdp/",
        "mypy-cdp"
    )
    
    # 7. Test documentation build (docs task)
    results['docs'] = test_command(
        "cd docs && make html",
        "docs"
    )
    
    # Summary
    print(f"\n=== Test Results Summary ===")
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for task, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{task:15} {status}")
    
    print(f"\nOverall: {passed}/{total} tasks passed")
    
    if passed == total:
        print("🎉 All pf tasks are working correctly!")
    else:
        print("⚠️  Some pf tasks need attention.")
        
    return results

if __name__ == "__main__":
    main()