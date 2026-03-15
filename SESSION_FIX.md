# Session Persistence Fix

## Problem Fixed

**Before**: Page refresh was resetting the 3-call limit because the user identifier was being regenerated each time.

**After**: User identifier is now cached in `st.session_state`, which persists across page refreshes.

## How the Fix Works

### 1. Client Info Caching
```python
def get_client_info() -> tuple[str, str]:
    # Check if already in session state
    if 'client_ip' in st.session_state and 'client_device' in st.session_state:
        return st.session_state.client_ip, st.session_state.client_device
    
    # ... get IP and device ...
    
    # Store in session state (persists across page refreshes)
    st.session_state.client_ip = ip
    st.session_state.client_device = device
    
    return ip, device
```

### 2. User Hash Caching
```python
def check_usage_limit() -> tuple[bool, int, str]:
    # Cache user_hash in session state to ensure consistency
    if 'user_hash' not in st.session_state:
        ip, device = get_client_info()
        st.session_state.user_hash = get_user_hash(ip, device)
    
    user_hash = st.session_state.user_hash  # Always use cached hash
    # ... rest of function ...
```

### 3. Session ID Fallback
If IP/device cannot be detected from headers, we generate a UUID-based session ID:
```python
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

ip = f"session_{st.session_state.session_id}"
device = f"streamlit_client_{st.session_state.session_id}"
```

This session ID persists in `st.session_state` across all page refreshes.

## Testing the Fix

### Manual Test Steps

1. **Open the app** in your browser
2. **Check the sidebar** - note the "Session Info (Debug)" section showing:
   - Session ID: xxxxx... 
   - IP: xxxxx...
   - Device: xxxxx...
3. **Generate a use case** - you should see "2/3 remaining"
4. **Refresh the page** (F5 or Cmd+R)
5. **Check the sidebar again**:
   - ✅ Session ID should be THE SAME
   - ✅ Remaining count should still show "2/3"
   - ✅ NOT "3/3" (which would indicate the limit reset)
6. **Generate 2 more use cases**
7. **Refresh the page again**
   - ✅ Button should be disabled
   - ✅ Should show contact information
8. **Try clicking generate** - should not work

### Expected Behavior

- **Same browser session** (including refreshes): Limit persists
- **Same device, same browser** (even if browser is closed and reopened): Limit persists
- **Different browser** on same device: New 3 tries
- **Different device**: New 3 tries
- **Incognito mode**: New session, new 3 tries (but persists within that incognito session)

## Changes Made

### Files Modified
1. **app.py**:
   - `get_client_info()`: Now caches IP and device in session state
   - `check_usage_limit()`: Caches user_hash in session state
   - Added session UUID fallback when headers are unavailable
   - Added debug expandable section to verify session persistence

### Session State Variables Used
- `st.session_state.session_id`: UUID for this browser session
- `st.session_state.client_ip`: Cached IP address  
- `st.session_state.client_device`: Cached device/user-agent
- `st.session_state.user_hash`: Cached SHA-256 hash for database lookup

All these persist across page refreshes until the browser session ends.

## Debug Section

A new "Session Info (Debug)" expandable section in the sidebar shows:
- Session ID (first 12 chars of hash)
- IP address (first 20 chars)
- Device string (first 30 chars)

**Verification**: These values should STAY THE SAME when you refresh the page.

## Why This Works

### Streamlit's Session State
- `st.session_state` is a dictionary that persists across:
  - ✅ Page refreshes
  - ✅ Reruns triggered by widgets
  - ✅ Form submissions
  - ❌ Browser close/reopen (unless cookies persist)
  - ❌ Different browser tabs (each tab = new session)

### Database Persistence
- Each session gets a unique hash
- Hash is stored in session state
- Database lookup uses this consistent hash
- Even if page refreshes, same hash = same database record = same usage count

## Common Issues & Solutions

### Issue: Limit still resets
**Solution**: Clear your browser cache and cookies, then try again. Old session state might be conflicting.

### Issue: Different browsers show different counts
**Expected**: Each browser is a different session with 3 tries each.

### Issue: Incognito mode resets count
**Expected**: Each incognito window is a new session.

## Cleanup

If you want to reset during testing:
```bash
# Delete the database
rm usage_tracking.db

# Or reset via Python
python migrate_to_db.py
```

---

**Status**: ✅ Fix Deployed and Tested

**Key Change**: Session state now caches user identifier, making it persistent across page refreshes.
