"""
Database module for Theory2Practice AI Bridge
Handles usage tracking with SQLite
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple
import hashlib

DB_FILE = Path("usage_tracking.db")

def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create usage table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_hash TEXT NOT NULL UNIQUE,
            ip_address TEXT,
            device_info TEXT,
            usage_count INTEGER DEFAULT 0,
            first_used TIMESTAMP,
            last_used TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create generation history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_hash TEXT NOT NULL,
            topic TEXT,
            field TEXT,
            difficulty_level TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_hash) REFERENCES usage_tracking(user_hash)
        )
    """)
    
    # Create index for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_hash 
        ON usage_tracking(user_hash)
    """)
    
    conn.commit()
    conn.close()

def get_user_hash(ip_address: str, device_info: str) -> str:
    """
    Generate a unique hash from IP and device info
    This ensures the same device from the same IP always gets the same hash
    """
    combined = f"{ip_address}|{device_info}"
    return hashlib.sha256(combined.encode()).hexdigest()

def get_usage_count(user_hash: str) -> int:
    """Get the current usage count for a user"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT usage_count FROM usage_tracking WHERE user_hash = ?",
        (user_hash,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else 0

def increment_usage(user_hash: str, ip_address: str, device_info: str, topic: str, field: str, difficulty_level: str) -> int:
    """
    Increment usage count for a user and log the generation
    Returns the new usage count
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    # Check if user exists
    cursor.execute(
        "SELECT usage_count, first_used FROM usage_tracking WHERE user_hash = ?",
        (user_hash,)
    )
    result = cursor.fetchone()
    
    if result:
        # Update existing user
        new_count = result[0] + 1
        cursor.execute("""
            UPDATE usage_tracking 
            SET usage_count = ?, last_used = ?, ip_address = ?, device_info = ?
            WHERE user_hash = ?
        """, (new_count, now, ip_address, device_info, user_hash))
    else:
        # Insert new user
        new_count = 1
        cursor.execute("""
            INSERT INTO usage_tracking (user_hash, ip_address, device_info, usage_count, first_used, last_used)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_hash, ip_address, device_info, new_count, now, now))
    
    # Log the generation
    cursor.execute("""
        INSERT INTO generation_history (user_hash, topic, field, difficulty_level)
        VALUES (?, ?, ?, ?)
    """, (user_hash, topic, field, difficulty_level))
    
    conn.commit()
    conn.close()
    
    return new_count

def get_statistics() -> Dict:
    """Get usage statistics for display"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Total unique users
    cursor.execute("SELECT COUNT(DISTINCT user_hash) FROM usage_tracking")
    total_users = cursor.fetchone()[0]
    
    # Total generations
    cursor.execute("SELECT SUM(usage_count) FROM usage_tracking")
    total_generations = cursor.fetchone()[0] or 0
    
    # Users who hit the limit
    cursor.execute("SELECT COUNT(*) FROM usage_tracking WHERE usage_count >= 3")
    users_at_limit = cursor.fetchone()[0]
    
    # Most popular topics
    cursor.execute("""
        SELECT topic, COUNT(*) as count 
        FROM generation_history 
        GROUP BY topic 
        ORDER BY count DESC 
        LIMIT 5
    """)
    popular_topics = cursor.fetchall()
    
    # Most popular fields
    cursor.execute("""
        SELECT field, COUNT(*) as count 
        FROM generation_history 
        GROUP BY field 
        ORDER BY count DESC 
        LIMIT 5
    """)
    popular_fields = cursor.fetchall()
    
    # Recent activity (last 24 hours)
    cursor.execute("""
        SELECT COUNT(*) FROM generation_history 
        WHERE generated_at > datetime('now', '-1 day')
    """)
    recent_activity = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_generations': total_generations,
        'users_at_limit': users_at_limit,
        'popular_topics': popular_topics,
        'popular_fields': popular_fields,
        'recent_activity': recent_activity
    }

def get_user_info(user_hash: str) -> Optional[Dict]:
    """Get detailed information about a user"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT user_hash, ip_address, device_info, usage_count, first_used, last_used
        FROM usage_tracking
        WHERE user_hash = ?
    """, (user_hash,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'user_hash': result[0],
            'ip_address': result[1],
            'device_info': result[2],
            'usage_count': result[3],
            'first_used': result[4],
            'last_used': result[5]
        }
    
    return None

def cleanup_old_data(days: int = 90):
    """Remove data older than specified days (for GDPR compliance)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM usage_tracking 
        WHERE last_used < datetime('now', ? || ' days')
    """, (f'-{days}',))
    
    conn.commit()
    conn.close()
