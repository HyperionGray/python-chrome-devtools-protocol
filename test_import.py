#!/usr/bin/env python3
# Test basic CDP import
try:
    import cdp
    print("✓ CDP import successful")
    print(f"CDP module location: {cdp.__file__}")
    
    # Test a specific module
    import cdp.accessibility
    print("✓ CDP accessibility module import successful")
    
except ImportError as e:
    print(f"✗ CDP import failed: {e}")
    exit(1)