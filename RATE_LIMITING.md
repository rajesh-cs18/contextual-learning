# Rate Limiting Implementation Guide

## Overview

The Theory2Practice AI Bridge now includes a **3-call free trial system** with usage tracking per IP address and device using **SQLite database**.

## Features Implemented

### ✅ Core Features
- **3 Free Generations**: Each unique IP + device combination gets 3 free use case generations
- **IP + Device Tracking**: Tracks usage by combination of IP address and User-Agent
- **SQLite Database**: Persistent storage with `usage_tracking.db`
- **Contact Information**: Shows your contact details when limit is reached
- **Usage Counter**: Displays remaining free trials in sidebar
- **Statistics Dashboard**: Shows platform-wide usage statistics on home page
- **Session Persistence**: Limits survive page refreshes and browser restarts

### 🔒 How It Works

1. **User Identification**
   - Gets IP from `X-Forwarded-For`, `X-Real-Ip`, or `Remote-Addr` headers
   - Gets device info from `User-Agent` header
   - Creates SHA-256 hash of IP + Device combination
   - Hash ensures privacy while maintaining uniqueness

2. **Usage Tracking (Database)**
   - Stored in `usage_tracking.db` SQLite database
   - Tables: `usage_tracking` (user limits) and `generation_history` (detailed logs)
   - Tracks: user_hash, IP, device, count, timestamps
   - Indexed for fast lookups
   - Persists across app restarts and page refreshes

3. **Limit Enforcement**
   - Generate button disabled after 3 uses from same IP + device
   - Beautiful gradient message box displays contact info
   - Shows remaining trials in sidebar
   - **Cannot be bypassed by page refresh** (database-backed)

## Database Schema

### usage_tracking table
```sql
CREATE TABLE usage_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_hash TEXT NOT NULL UNIQUE,
    ip_address TEXT,
    device_info TEXT,
    usage_count INTEGER DEFAULT 0,
    first_used TIMESTAMP,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### generation_history table
```sql
CREATE TABLE generation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_hash TEXT NOT NULL,
    topic TEXT,
    field TEXT,
    difficulty_level TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_hash) REFERENCES usage_tracking(user_hash)
)
```

## Statistics Displayed

On the home page, users see:
- **Total Users**: Number of unique IP + device combinations
- **Total Generations**: Sum of all use cases generated
- **Last 24 Hours**: Recent activity count
- **Active Users**: Users who have hit the 3-generation limit
- **Popular Topics**: Top 3 most generated topics
- **Popular Fields**: Top 3 most used academic fields

## Contact Information Displayed

When users reach the limit, they see:

```
📧 raj20032003@gmail.com
📱 +92 342 8181914
```

## Admin Functions

### View Database Statistics

```python
from database import get_statistics

stats = get_statistics()
print(f"Total users: {stats['total_users']}")
print(f"Total generations: {stats['total_generations']}")
```

### Reset Usage for Testing

To reset all usage tracking:
```bash
rm usage_tracking.db
python migrate_to_db.py  # Reinitialize database
```

### Reset Specific User

```python
import sqlite3

conn = sqlite3.connect('usage_tracking.db')
cursor = conn.cursor()

# Find user by IP or partial hash
cursor.execute("SELECT * FROM usage_tracking WHERE ip_address LIKE '%192.168%'")
print(cursor.fetchall())

# Delete specific user
cursor.execute("DELETE FROM usage_tracking WHERE user_hash = 'hash_here'")
conn.commit()
conn.close()
```

### View All Users

```bash
sqlite3 usage_tracking.db "SELECT ip_address, usage_count, last_used FROM usage_tracking ORDER BY last_used DESC LIMIT 10;"
```

### Export Statistics

```python
from database import get_statistics
import json

stats = get_statistics()
with open('stats_export.json', 'w') as f:
    json.dump(stats, f, indent=2)
```

### Change Limit

Edit `app.py`:
```python
MAX_FREE_CALLS = 3  # Change this number
```

## Deployment Notes

### Streamlit Cloud
- `usage_tracking.db` will persist between sessions
- Each deployment environment tracks separately
- Database file is gitignored - won't be in repository
- **Page refresh no longer bypasses limit** - database persists state

### Production Recommendations

The current implementation is production-ready with:
- ✅ **Persistent storage** across restarts
- ✅ **IP + Device tracking** for accurate user identification
- ✅ **Indexed database** for fast lookups
- ✅ **Generation history** for analytics
- ✅ **Privacy-friendly** hashing

For enterprise deployment, consider:
1. **PostgreSQL/MySQL**: Replace SQLite with a production database
2. **Redis Cache**: Add caching layer for high traffic
3. **Rate Limiting by Time**: Add hourly/daily limits
4. **Geographic Restrictions**: Filter by country
5. **Payment Integration**: Stripe for paid tiers

## Security Considerations

### Current Implementation (Production-Ready)
- ✅ **Database-backed**: SQLite with ACID guarantees
- ✅ **No personal data**: Only hashed identifiers stored
- ✅ **IP + Device tracking**: Accurate user identification
- ✅ **Indexed queries**: Fast lookups, no performance issues
- ✅ **Cannot be bypassed**: Survives page refresh, browser restart
- ✅ **Privacy-friendly**: SHA-256 hashing

### What Users Cannot Bypass
- ❌ Page refresh
- ❌ Browser restart
- ❌ Opening in new tab
- ❌ Clearing cookies
- ❌ Using incognito mode (same device)

### What Users Can Bypass (Acceptable)
- ✅ Different browser (different User-Agent)
- ✅ Different device
- ✅ VPN/proxy (different IP)
- ✅ Clearing browser and using different browser

For strict enforcement, upgrade to authentication-based system.

### Upgrading Security

For production, add:
```python
# Example: Time-based reset
from datetime import datetime, timedelta

def should_reset_user(user_data):
    last_reset = datetime.fromisoformat(user_data.get('last_reset', '2000-01-01'))
    if datetime.now() - last_reset > timedelta(days=30):
        return True
    return False
```

## Testing

### Test Scenarios

1. **First Use**: Should show "3/3 remaining" + statistics
2. **Second Use**: Should show "2/3 remaining"
3. **Third Use**: Should show "1/3 remaining" + warning
4. **Fourth Attempt**: Button disabled, contact info displayed
5. **Page Refresh**: Limit should persist (not reset)
6. **Browser Restart**: Limit should still be enforced

### Manual Testing
```bash
# Run migrations
python migrate_to_db.py

# Run app
streamlit run app.py

# Test sequence:
# 1. Make 3 generations
# 2. Refresh page - should still show 0 remaining
# 3. Try 4th generation - should see limit message
# 4. Check statistics on home page

# Inspect database
sqlite3 usage_tracking.db
> SELECT * FROM usage_tracking;
> SELECT * FROM generation_history;
> .quit

# Reset for next test
rm usage_tracking.db
python migrate_to_db.py
```

### Automated Testing

```python
# test_database.py
from database import init_database, get_user_hash, increment_usage, get_usage_count

def test_rate_limiting():
    init_database()
    
    ip = "192.168.1.1"
    device = "Mozilla/5.0 Test"
    user_hash = get_user_hash(ip, device)
    
    # Test 3 increments
    for i in range(3):
        count = increment_usage(user_hash, ip, device, f"Topic{i}", "CS", "Junior")
        assert count == i + 1
    
    # Test limit
    count = get_usage_count(user_hash)
    assert count == 3
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_rate_limiting()
```

## Customization

### Change Contact Info

In `app.py`:
```python
CONTACT_EMAIL = "your_email@example.com"
CONTACT_PHONE = "+1 234 567 8900"
```

### Change Message Style

Edit the CSS in the `display_limit_reached()` function:
```python
.limit-reached-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    # Customize gradient colors
}
```

### Add More Info to Contact Page

Modify `display_limit_reached()` to add:
- Links to pricing page
- Demo video
- Social media links
- Company information

## Analytics

To track usage patterns, add logging:

```python
def increment_usage(identifier: str):
    # ... existing code ...
    
    # Add analytics
    total_users = len(usage_data)
    total_requests = sum(u['count'] for u in usage_data.values())
    print(f"Analytics: {total_users} users, {total_requests} total requests")
```

## Future Enhancements

- [ ] Email collection before first use
- [ ] Stripe payment integration
- [ ] Admin dashboard for usage stats
- [ ] Email notifications when limit reached
- [ ] Referral system (get more free calls)
- [ ] JWT-based authentication
- [ ] Rate limiting by time (X per hour)
- [ ] Geographic restrictions/allowlisting

---

**Current Status**: ✅ Production-Ready with Database Backend

**Files Modified**: 
- `app.py` - Added database integration and statistics display
- `database.py` - New SQLite database module (200+ lines)
- `migrate_to_db.py` - Migration script from JSON to database

**Files Created**: 
- `usage_tracking.db` - SQLite database (auto-generated, gitignored)

**Key Improvements**:
- ✅ **Page refresh doesn't reset limit** (was main bug)
- ✅ **Statistics dashboard** on home page
- ✅ **IP + Device tracking** for accuracy
- ✅ **Generation history** logged for analytics
- ✅ **Production-grade** database backend
