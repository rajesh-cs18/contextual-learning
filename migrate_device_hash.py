"""
Migration script to consolidate duplicate users
Merges users with same device but different IPs into single entries
Run this once after updating the hashing logic
"""

import sqlite3
from pathlib import Path
import hashlib
from datetime import datetime

DB_FILE = Path("usage_tracking.db")

def migrate_to_device_based_hash():
    """Consolidate users based on device fingerprint instead of IP+device"""
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("🔄 Starting migration to device-based user tracking...")
    
    # Get all current users
    cursor.execute("""
        SELECT id, user_hash, ip_address, device_info, usage_count, first_used, last_used
        FROM usage_tracking
        ORDER BY device_info, first_used
    """)
    
    users = cursor.fetchall()
    print(f"📊 Found {len(users)} total entries")
    
    # Group by device_info
    device_groups = {}
    for user in users:
        user_id, old_hash, ip, device, count, first, last = user
        
        if device not in device_groups:
            device_groups[device] = []
        
        device_groups[device].append({
            'id': user_id,
            'old_hash': old_hash,
            'ip': ip,
            'device': device,
            'count': count,
            'first_used': first,
            'last_used': last
        })
    
    # Find duplicates
    duplicates = {device: entries for device, entries in device_groups.items() if len(entries) > 1}
    
    if duplicates:
        print(f"🔍 Found {len(duplicates)} devices with multiple entries")
        
        for device, entries in duplicates.items():
            print(f"\n📱 Device: {device[:80]}...")
            print(f"   Consolidating {len(entries)} entries:")
            
            # Calculate consolidated values
            new_hash = hashlib.sha256(device.encode()).hexdigest()
            total_count = sum(e['count'] for e in entries)
            latest_ip = entries[-1]['ip']  # Use most recent IP
            earliest_first = min(e['first_used'] for e in entries)
            latest_last = max(e['last_used'] for e in entries)
            old_hashes = [e['old_hash'] for e in entries]
            
            print(f"   - Old hashes: {len(old_hashes)} different")
            print(f"   - New hash: {new_hash[:16]}...")
            print(f"   - Total usage: {total_count}")
            print(f"   - IP addresses: {[e['ip'] for e in entries]}")
            
            # Delete old entries
            for entry in entries:
                cursor.execute("DELETE FROM usage_tracking WHERE id = ?", (entry['id'],))
            
            # Update generation history to use new hash
            for old_hash in old_hashes:
                cursor.execute("""
                    UPDATE generation_history 
                    SET user_hash = ? 
                    WHERE user_hash = ?
                """, (new_hash, old_hash))
            
            # Insert consolidated entry
            cursor.execute("""
                INSERT INTO usage_tracking 
                (user_hash, ip_address, device_info, usage_count, first_used, last_used, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (new_hash, latest_ip, device, total_count, earliest_first, latest_last, datetime.now().isoformat()))
            
            print(f"   ✅ Consolidated into 1 entry")
    
    else:
        print("✅ No duplicates found")
    
    # Update remaining single entries to use new hash
    single_devices = {device: entries[0] for device, entries in device_groups.items() if len(entries) == 1}
    
    if single_devices:
        print(f"\n🔄 Updating {len(single_devices)} single entries to new hash format...")
        
        for device, entry in single_devices.items():
            new_hash = hashlib.sha256(device.encode()).hexdigest()
            old_hash = entry['old_hash']
            
            if new_hash != old_hash:
                # Update usage_tracking
                cursor.execute("""
                    UPDATE usage_tracking 
                    SET user_hash = ? 
                    WHERE id = ?
                """, (new_hash, entry['id']))
                
                # Update generation_history
                cursor.execute("""
                    UPDATE generation_history 
                    SET user_hash = ? 
                    WHERE user_hash = ?
                """, (new_hash, old_hash))
    
    conn.commit()
    
    # Verify results
    cursor.execute("SELECT COUNT(*) FROM usage_tracking")
    final_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT device_info) FROM usage_tracking")
    unique_devices = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n✅ Migration complete!")
    print(f"📊 Final statistics:")
    print(f"   - Total entries: {final_count}")
    print(f"   - Unique devices: {unique_devices}")
    print(f"   - Duplicates removed: {len(users) - final_count}")

if __name__ == "__main__":
    if not DB_FILE.exists():
        print("❌ Database file not found!")
        exit(1)
    
    response = input("⚠️  This will modify the database. Continue? (yes/no): ")
    if response.lower() == 'yes':
        migrate_to_device_based_hash()
        print("\n🎉 Migration successful! Users with same device are now consolidated.")
    else:
        print("Migration cancelled.")
