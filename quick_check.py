import subprocess
import sys
import os

# Simple environment and basic test check
print("=== Environment Check ===")

# Check Python
try:
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
except Exception as e:
    print(f"Python check failed: {e}")

# Check current directory
print(f"Current directory: {os.getcwd()}")
print(f"Workspace contents: {os.listdir('/workspace')[:10]}...")

# Check if we can import CDP
print("\n=== CDP Import Test ===")
try:
    sys.path.insert(0, '/workspace')
    import cdp
    print("✓ CDP import successful")
    
    # Try importing a specific module
    import cdp.runtime
    print("✓ CDP.runtime import successful")
    
    # Check if we have the basic structure
    print(f"CDP module file: {cdp.__file__}")
    
except Exception as e:
    print(f"✗ CDP import failed: {e}")
    import traceback
    traceback.print_exc()

# Check for required tools
print("\n=== Tool Availability ===")
tools = ['pytest', 'mypy']
for tool in tools:
    try:
        result = subprocess.run([sys.executable, '-m', tool, '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ {tool} available: {result.stdout.strip()}")
        else:
            print(f"✗ {tool} not working: {result.stderr.strip()}")
    except Exception as e:
        print(f"✗ {tool} check failed: {e}")

print("\n=== Basic Test Run ===")
# Try running a simple test
try:
    os.chdir('/workspace')
    result = subprocess.run([sys.executable, '-c', 'import cdp; print("Import test passed")'], 
                          capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("✓ Basic import test passed")
    else:
        print(f"✗ Basic import test failed: {result.stderr}")
except Exception as e:
    print(f"✗ Basic test failed: {e}")