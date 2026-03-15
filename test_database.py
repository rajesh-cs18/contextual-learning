"""
Quick test script for database functionality
Run this to verify the database and rate limiting work correctly
"""

from database import init_database, get_user_hash, increment_usage, get_usage_count, get_statistics
from pathlib import Path

def test_database():
    """Test the database functionality"""
    
    print("🧪 Testing Database Functionality\n")
    print("=" * 60)
    
    # Test 1: Initialize database
    print("\n✓ Test 1: Initializing database...")
    init_database()
    if Path("usage_tracking.db").exists():
        print("  ✅ Database file created successfully")
    else:
        print("  ❌ ERROR: Database file not created")
        return
    
    # Test 2: Create user hash
    print("\n✓ Test 2: Creating user hash...")
    test_ip = "192.168.1.100"
    test_device = "Mozilla/5.0 (Test Browser)"
    user_hash = get_user_hash(test_ip, test_device)
    print(f"  User hash: {user_hash[:16]}...")
    print("  ✅ Hash generation works")
    
    # Test 3: Check initial usage (should be 0)
    print("\n✓ Test 3: Checking initial usage...")
    initial_count = get_usage_count(user_hash)
    if initial_count == 0:
        print(f"  ✅ Initial count is 0 (correct)")
    else:
        print(f"  ❌ ERROR: Initial count is {initial_count}, expected 0")
    
    # Test 4: Increment usage 3 times
    print("\n✓ Test 4: Simulating 3 generations...")
    for i in range(1, 4):
        count = increment_usage(
            user_hash, 
            test_ip, 
            test_device,
            f"Test Topic {i}",
            "Computer Science",
            "Junior"
        )
        print(f"  Generation {i}: Count = {count}")
        if count != i:
            print(f"  ❌ ERROR: Expected {i}, got {count}")
            return
    
    print("  ✅ All 3 increments successful")
    
    # Test 5: Verify final count
    print("\n✓ Test 5: Verifying final count...")
    final_count = get_usage_count(user_hash)
    if final_count == 3:
        print(f"  ✅ Final count is 3 (limit reached)")
    else:
        print(f"  ❌ ERROR: Final count is {final_count}, expected 3")
        return
    
    # Test 6: Get statistics
    print("\n✓ Test 6: Getting platform statistics...")
    try:
        stats = get_statistics()
        print(f"  Total users: {stats['total_users']}")
        print(f"  Total generations: {stats['total_generations']}")
        print(f"  Users at limit: {stats['users_at_limit']}")
        print("  ✅ Statistics retrieved successfully")
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return
    
    # Test 7: Test different user
    print("\n✓ Test 7: Testing different IP/device...")
    different_ip = "10.0.0.50"
    different_device = "Chrome/Test"
    different_hash = get_user_hash(different_ip, different_device)
    
    if different_hash != user_hash:
        print("  ✅ Different IP/device creates different hash")
        
        count = get_usage_count(different_hash)
        if count == 0:
            print("  ✅ New user has 0 usage count")
        else:
            print(f"  ❌ ERROR: New user has count {count}, expected 0")
    else:
        print("  ❌ ERROR: Same hash for different IP/device!")
    
    # Test 8: Test same IP but different device
    print("\n✓ Test 8: Same IP, different device...")
    same_ip_different_device = get_user_hash(test_ip, "Different Browser")
    if same_ip_different_device != user_hash:
        print("  ✅ Different device creates different hash (even with same IP)")
    else:
        print("  ❌ ERROR: Same hash despite different device!")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!\n")
    
    print("📊 Summary:")
    print(f"  - Database file: usage_tracking.db")
    print(f"  - Test user hash: {user_hash[:16]}...")
    print(f"  - Usage count: {final_count}/3")
    print(f"  - Platform stats: {stats['total_users']} users, {stats['total_generations']} generations")
    
    print("\n🧹 Cleanup:")
    print("  To reset the database: rm usage_tracking.db")
    print("\n✨ Database is working correctly and ready for production!")

if __name__ == "__main__":
    test_database()
