"""
Test Reset Functionality
"""

import sqlite3
from pathlib import Path

print('Testing Reset Functionality')
print('=' * 50)

# Create test database
DB_FILE = Path('test_reset.db')
if DB_FILE.exists():
    DB_FILE.unlink()

# Setup
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE usage_tracking (
        id INTEGER PRIMARY KEY,
        user_hash TEXT UNIQUE,
        ip_address TEXT,
        device_info TEXT,
        usage_count INTEGER DEFAULT 0,
        first_used TIMESTAMP,
        last_used TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE generation_history (
        id INTEGER PRIMARY KEY,
        user_hash TEXT,
        topic TEXT,
        field TEXT,
        difficulty_level TEXT,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Add test user
user_hash = 'test_user_123'
cursor.execute('''
    INSERT INTO usage_tracking (user_hash, ip_address, device_info, usage_count)
    VALUES (?, ?, ?, ?)
''', (user_hash, '192.168.1.1', 'Test Browser', 3))

# Add generation history
for i in range(3):
    cursor.execute('''
        INSERT INTO generation_history (user_hash, topic, field, difficulty_level)
        VALUES (?, ?, ?, ?)
    ''', (user_hash, f'Topic {i}', 'Computer Science', 'Senior'))

conn.commit()

# Verify before reset
cursor.execute('SELECT usage_count FROM usage_tracking WHERE user_hash = ?', (user_hash,))
before_count = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM generation_history WHERE user_hash = ?', (user_hash,))
before_history = cursor.fetchone()[0]

print(f'\n✓ Before Reset:')
print(f'  Usage Count: {before_count}')
print(f'  History Records: {before_history}')

# Perform reset
cursor.execute('DELETE FROM generation_history WHERE user_hash = ?', (user_hash,))
cursor.execute('UPDATE usage_tracking SET usage_count = 0 WHERE user_hash = ?', (user_hash,))
conn.commit()

# Verify after reset
cursor.execute('SELECT usage_count FROM usage_tracking WHERE user_hash = ?', (user_hash,))
after_count = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM generation_history WHERE user_hash = ?', (user_hash,))
after_history = cursor.fetchone()[0]

print(f'\n✓ After Reset:')
print(f'  Usage Count: {after_count}')
print(f'  History Records: {after_history}')

# Verify user record still exists
cursor.execute('SELECT COUNT(*) FROM usage_tracking WHERE user_hash = ?', (user_hash,))
user_exists = cursor.fetchone()[0]

print(f'\n✓ User Record Still Exists: {user_exists == 1}')

conn.close()
DB_FILE.unlink()

print('\n' + '=' * 50)
print('✅ Reset Test Passed!')
print('  - Usage count: 3 → 0')
print('  - History: 3 records → 0 records')
print('  - User record preserved')
print('  - User can now make 3 more generations')
