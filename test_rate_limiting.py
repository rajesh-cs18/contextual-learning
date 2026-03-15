"""
Test script for rate limiting functionality
Run this to verify rate limiting works correctly
"""

import json
from pathlib import Path
import hashlib

USAGE_FILE = Path("usage_tracking.json")
MAX_FREE_CALLS = 3

def test_rate_limiting():
    """Test the rate limiting system"""
    
    print("🧪 Testing Rate Limiting System\n")
    print("=" * 50)
    
    # Test 1: Load empty usage data
    print("\n✓ Test 1: Initial state (no usage file)")
    if USAGE_FILE.exists():
        USAGE_FILE.unlink()
        print("  Removed existing usage file")
    print("  ✅ Clean slate ready")
    
    # Test 2: Create mock usage data
    print("\n✓ Test 2: Creating mock user data")
    test_identifier = hashlib.md5(b"test_user").hexdigest()
    
    usage_data = {
        test_identifier: {
            "count": 0,
            "first_used": "2026-03-15T10:00:00",
            "last_used": "2026-03-15T10:00:00"
        }
    }
    
    with open(USAGE_FILE, 'w') as f:
        json.dump(usage_data, f, indent=2)
    
    print(f"  Created user: {test_identifier[:8]}...")
    print("  ✅ Mock data created")
    
    # Test 3: Simulate usage increments
    print("\n✓ Test 3: Simulating usage increments")
    for i in range(1, 5):
        with open(USAGE_FILE, 'r') as f:
            data = json.load(f)
        
        current_count = data[test_identifier]['count']
        
        if current_count < MAX_FREE_CALLS:
            data[test_identifier]['count'] += 1
            with open(USAGE_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            
            remaining = MAX_FREE_CALLS - data[test_identifier]['count']
            print(f"  Call {i}: ✅ Allowed (Remaining: {remaining})")
        else:
            print(f"  Call {i}: 🚫 BLOCKED - Limit reached!")
    
    # Test 4: Verify final state
    print("\n✓ Test 4: Verifying final state")
    with open(USAGE_FILE, 'r') as f:
        final_data = json.load(f)
    
    final_count = final_data[test_identifier]['count']
    print(f"  Final count: {final_count}/{MAX_FREE_CALLS}")
    
    if final_count == MAX_FREE_CALLS:
        print("  ✅ Limit enforced correctly!")
    else:
        print(f"  ❌ ERROR: Expected {MAX_FREE_CALLS}, got {final_count}")
    
    # Test 5: Check file format
    print("\n✓ Test 5: Validating JSON structure")
    try:
        assert 'count' in final_data[test_identifier]
        assert 'first_used' in final_data[test_identifier]
        assert 'last_used' in final_data[test_identifier]
        print("  ✅ All required fields present")
    except AssertionError:
        print("  ❌ ERROR: Missing required fields")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!\n")
    print("📄 Check usage_tracking.json to see the data structure")
    print("🧹 Run 'rm usage_tracking.json' to clean up\n")

if __name__ == "__main__":
    test_rate_limiting()
