"""
Migration script from JSON-based tracking to SQLite database
Run this once to migrate existing data (if any) from usage_tracking.json to the database
"""

import json
from pathlib import Path
from database import init_database, get_user_hash, increment_usage
from datetime import datetime

JSON_FILE = Path("usage_tracking.json")

def migrate_json_to_db():
    """Migrate data from JSON file to SQLite database"""
    
    print("🔄 Starting migration from JSON to SQLite...")
    
    # Initialize database
    init_database()
    print("✅ Database initialized")
    
    # Check if JSON file exists
    if not JSON_FILE.exists():
        print("ℹ️  No JSON file found - starting fresh with database")
        return
    
    # Load JSON data
    try:
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
        
        print(f"📊 Found {len(data)} entries in JSON file")
        
        # Note: JSON data doesn't have IP/device info, so we can't migrate it perfectly
        # We'll just note that migration isn't needed for new database-based system
        print("⚠️  Note: Old JSON data structure is incompatible with new database")
        print("   Starting fresh with database - old limits will not carry over")
        
        # Optionally backup the JSON file
        backup_file = JSON_FILE.with_suffix('.json.backup')
        JSON_FILE.rename(backup_file)
        print(f"📦 Old JSON file backed up to: {backup_file}")
        print("   You can delete this file if everything works correctly")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return
    
    print("✅ Migration complete! Database is ready to use.")
    print("\n💡 Note: All users will start fresh with 3 free generations")
    print("   This is because the new system tracks by IP + Device for better accuracy")

if __name__ == "__main__":
    migrate_json_to_db()
