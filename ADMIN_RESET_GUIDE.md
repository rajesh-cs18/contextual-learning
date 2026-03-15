# Admin Dashboard - User Reset Guide

This guide explains all the user reset functionalities available in the Admin Dashboard.

## 🎯 Quick Access

1. **Login to Admin Dashboard**: Navigate to "🔐 Admin Dashboard" in the sidebar
2. **Use credentials**: Username: `rajesh`, Password: `11224433`

---

## 🔄 Reset Options Overview

### 1. **Users Tab - Quick Actions**

#### Reset All Users at Limit
- **Location**: Top of Users tab
- **Button**: "🔄 Reset All Users at Limit (N)"
- **Action**: Resets all users who have used 3/3 generations
- **Use Case**: Monthly/weekly cleanup to give users fresh access

#### Reset ALL Users
- **Location**: Top of Users tab  
- **Button**: "🔄 Reset ALL Users to 0"
- **Action**: Resets every user back to 0 usage
- **Confirmation**: Click twice to confirm
- **Use Case**: New semester, new campaign, or promotional period

#### Individual Reset (Inline)
- **Location**: Each user row has a 🔄 button
- **Action**: Reset that specific user instantly
- **Use Case**: Customer support - giving individual users another chance

---

### 2. **Search Tab - Find and Reset**

#### Search by IP Address
- **Input**: Enter full or partial IP (e.g., "192.168" or "192.168.1.100")
- **Results**: Shows all users from that IP
- **Quick Actions**:
  - "🔄 Reset All N Users" - Reset all found users
  - "🗑️ Delete All N Users" - Permanently delete all found users
- **Use Case**: School/office network - reset all users from same location

#### Search by User Hash
- **Input**: Enter full or partial hash
- **Results**: Shows user details + generation history
- **Quick Actions**: 
  - "🔄 Reset" button per user
  - "🗑️ Delete" button per user
- **Use Case**: Find specific user by their unique identifier

---

### 3. **Admin Actions Tab - Bulk Management**

#### Reset by Usage Count
- **Input**: Minimum usage threshold (1-3)
- **Example**: Set to "2" to reset all users with ≥2 generations
- **Button**: "🔄 Reset N Users (>= X uses)"
- **Use Case**: Give extra access to power users

#### Reset Inactive Users
- **Input**: Number of days inactive (1-365)
- **Example**: "30" to reset users who haven't used the app in 30+ days
- **Button**: "🔄 Reset Users Inactive > N days"
- **Use Case**: Clear out old/abandoned accounts

#### Reset Specific User
- **Select**: Choose user from dropdown
- **Display**: Shows IP, usage count, and hash preview
- **Button**: "🔄 Reset User Count to 0"
- **Use Case**: Individual customer support requests

#### Delete Specific User
- **Select**: Choose user from dropdown
- **Button**: "🗑️ Delete User Permanently"
- **Warning**: Deletes user AND their history - cannot be undone
- **Use Case**: Remove test accounts or spam users

---

### 4. **Dangerous Actions** 🚨

#### Reset ALL Users to 0
- **Button**: "🔄 Reset ALL Users to 0"
- **Confirmation**: Click twice to confirm
- **Action**: 
  - Sets all usage counts to 0
  - Deletes ALL generation history
  - Keeps user records (IP, device, timestamps)
- **Use Case**: Monthly reset, promotional period

#### Clear All Data (Delete Everything)
- **Button**: "🗑️ Clear All Data (Delete Everything)"
- **Confirmation**: Click twice to confirm
- **Action**: 
  - Deletes ALL users
  - Deletes ALL generation history
  - Completely empty database
- **Use Case**: Fresh start, testing, database cleanup

---

## 📊 What Gets Reset vs Deleted

### Reset (🔄)
- ✅ Usage count → 0
- ✅ Generation history → Deleted
- ❌ User record → **Kept** (IP, device, first_used, last_used)
- **Result**: User can make 3 more generations

### Delete (🗑️)
- ✅ Usage count → Gone
- ✅ Generation history → Gone
- ✅ User record → **Deleted completely**
- **Result**: User treated as brand new on next visit

---

## 💡 Best Practices

### Regular Maintenance
- **Weekly**: Review users at limit, reset trusted users
- **Monthly**: Reset all users at limit or reset all users completely
- **Quarterly**: Clean up inactive users (>90 days)

### Customer Support
1. User requests more access → Search by IP → Reset individual user
2. School/office wants access → Search by IP → Reset all users from that IP
3. Promotional event → Admin Actions → Reset ALL users

### Testing
- Use "Delete" for test accounts to keep data clean
- Use "Reset" for real users to preserve analytics

---

## 🔒 Security

- All actions require admin login (username: rajesh)
- Dangerous actions require double-click confirmation
- Actions cannot be undone - database backups recommended
- All resets are logged in the database timestamps

---

## 📞 Contact

For questions about reset policies or bulk operations:
- 📧 raj20032003@gmail.com
- 📱 +92 342 8181914
