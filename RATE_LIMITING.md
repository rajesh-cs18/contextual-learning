# Rate Limiting Implementation Guide

## Overview

The Theory2Practice AI Bridge now includes a **3-call free trial system** with usage tracking per device/IP.

## Features Implemented

### ✅ Core Features
- **3 Free Generations**: Each user gets 3 free use case generations
- **Device/Session Tracking**: Tracks usage by session identifier
- **Persistent Storage**: Usage data saved to `usage_tracking.json`
- **Contact Information**: Shows your contact details when limit is reached
- **Usage Counter**: Displays remaining free trials in sidebar

### 🔒 How It Works

1. **User Identification**
   - Attempts to get IP from request headers
   - Falls back to session-based UUID if IP unavailable
   - Identifier is hashed for privacy

2. **Usage Tracking**
   - Stored in `usage_tracking.json` (gitignored)
   - Tracks: count, first_used, last_used timestamps
   - Persists across app restarts

3. **Limit Enforcement**
   - Generate button disabled after 3 uses
   - Beautiful gradient message box displays contact info
   - Shows remaining trials in sidebar

## Contact Information Displayed

When users reach the limit, they see:

```
📧 raj20032003@gmail.com
📱 +92 342 8181914
```

## Admin Functions

### Reset Usage for Testing

To reset all usage tracking:
```bash
rm usage_tracking.json
```

### Reset Specific User

Edit `usage_tracking.json` and remove their entry (identified by hash).

### Change Limit

Edit `app.py`:
```python
MAX_FREE_CALLS = 3  # Change this number
```

## Deployment Notes

### Streamlit Cloud
- `usage_tracking.json` will persist between sessions
- Each deployment environment tracks separately
- Users can bypass by clearing browser data (acceptable for demo)

### Production Recommendations

For serious production use, consider:

1. **Database Storage**: Use PostgreSQL/MongoDB instead of JSON file
2. **IP-Based Tracking**: Implement proper IP detection behind proxies
3. **Time-Based Limits**: Reset limits daily/weekly
4. **Payment Integration**: Add Stripe for paid access
5. **Authentication**: Require login for tracking

## Security Considerations

### Current Implementation (Good for Demo)
- ✅ Simple and effective
- ✅ No personal data collected
- ✅ Hashed identifiers
- ✅ File-based (no DB needed)

### Limitations
- ⚠️ Can be bypassed by clearing browser data
- ⚠️ Not suitable for paid services
- ⚠️ No account management

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

1. **First Use**: Should show "3/3 remaining"
2. **Second Use**: Should show "2/3 remaining"
3. **Third Use**: Should show "1/3 remaining" + warning
4. **Fourth Attempt**: Button disabled, contact info displayed

### Manual Testing
```bash
# Run app
streamlit run app.py

# Make 3 generations
# Try 4th generation - should see limit message

# Reset for next test
rm usage_tracking.json
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

**Current Status**: ✅ Implemented and Ready

**File Modified**: `app.py` (added ~150 lines for rate limiting)

**Files Created**: `usage_tracking.json` (auto-generated, gitignored)
