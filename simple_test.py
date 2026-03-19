import sys
import os

# Add current directory to path
sys.path.insert(0, '/workspace')

try:
    import cdp
    print("✓ CDP import successful")
    print(f"CDP module: {cdp}")
    
    # Test specific module
    import cdp.accessibility
    print("✓ CDP accessibility import successful")
    
    # Test another module
    import cdp.runtime
    print("✓ CDP runtime import successful")
    
    print("✓ All basic imports working")
    
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()