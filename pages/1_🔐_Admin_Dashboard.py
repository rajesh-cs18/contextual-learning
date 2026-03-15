"""
Admin Dashboard for Theory2Practice AI Bridge
View and manage usage tracking data
"""

import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv
import hashlib

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard - Theory2Practice",
    page_icon="🔐",
    layout="wide"
)

# Authentication credentials from .env
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_authentication() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def login():
    """Display login form and handle authentication"""
    st.markdown("# 🔐 Admin Login")
    st.markdown("*Please enter your credentials to access the admin dashboard*")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH:
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.rerun()

DB_FILE = Path("usage_tracking.db")

# Check authentication first
if not check_authentication():
    login()
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
        logout()
    st.markdown(f"*Logged in as: {ADMIN_USERNAME}*")


def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_FILE)

def load_usage_data():
    """Load all usage tracking data"""
    conn = get_connection()
    query = """
        SELECT 
            id,
            user_hash,
            ip_address,
            device_info,
            usage_count,
            first_used,
            last_used,
            created_at
        FROM usage_tracking
        ORDER BY last_used DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def load_generation_history():
    """Load all generation history"""
    conn = get_connection()
    query = """
        SELECT 
            gh.id,
            gh.user_hash,
            ut.ip_address,
            gh.topic,
            gh.field,
            gh.difficulty_level,
            gh.generated_at
        FROM generation_history gh
        LEFT JOIN usage_tracking ut ON gh.user_hash = ut.user_hash
        ORDER BY gh.generated_at DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_summary_stats():
    """Get summary statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    # Total users
    cursor.execute("SELECT COUNT(*) FROM usage_tracking")
    stats['total_users'] = cursor.fetchone()[0]
    
    # Total generations
    cursor.execute("SELECT SUM(usage_count) FROM usage_tracking")
    stats['total_generations'] = cursor.fetchone()[0] or 0
    
    # Users at limit
    cursor.execute("SELECT COUNT(*) FROM usage_tracking WHERE usage_count >= 3")
    stats['users_at_limit'] = cursor.fetchone()[0]
    
    # Active users (last 24h)
    cursor.execute("""
        SELECT COUNT(*) FROM generation_history 
        WHERE generated_at > datetime('now', '-1 day')
    """)
    stats['active_24h'] = cursor.fetchone()[0]
    
    # Active users (last 7 days)
    cursor.execute("""
        SELECT COUNT(*) FROM generation_history 
        WHERE generated_at > datetime('now', '-7 days')
    """)
    stats['active_7d'] = cursor.fetchone()[0]
    
    conn.close()
    return stats

def delete_user(user_hash):
    """Delete a user and their history"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM generation_history WHERE user_hash = ?", (user_hash,))
    cursor.execute("DELETE FROM usage_tracking WHERE user_hash = ?", (user_hash,))
    
    conn.commit()
    conn.close()

def reset_user_count(user_hash):
    """Reset a user's usage count to 0"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Delete their generation history
    cursor.execute("DELETE FROM generation_history WHERE user_hash = ?", (user_hash,))
    # Reset usage count to 0
    cursor.execute("UPDATE usage_tracking SET usage_count = 0 WHERE user_hash = ?", (user_hash,))
    
    conn.commit()
    conn.close()

def reset_multiple_users(user_hashes: list):
    """Reset multiple users' usage counts to 0"""
    conn = get_connection()
    cursor = conn.cursor()
    
    for user_hash in user_hashes:
        cursor.execute("DELETE FROM generation_history WHERE user_hash = ?", (user_hash,))
        cursor.execute("UPDATE usage_tracking SET usage_count = 0 WHERE user_hash = ?", (user_hash,))
    
    conn.commit()
    conn.close()
    return len(user_hashes)

# Title
st.title("🔐 Admin Dashboard")
st.markdown("*Database Management for Theory2Practice AI Bridge*")

# Check if database exists
if not DB_FILE.exists():
    st.error("❌ Database not found! Please run the app first to create the database.")
    st.stop()

# Summary Statistics
st.markdown("---")
st.markdown("## 📊 Summary Statistics")

stats = get_summary_stats()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Users", stats['total_users'])

with col2:
    st.metric("Total Generations", stats['total_generations'])

with col3:
    st.metric("Users at Limit", stats['users_at_limit'])

with col4:
    st.metric("Active (24h)", stats['active_24h'])

with col5:
    st.metric("Active (7d)", stats['active_7d'])

# Tabs for different views
st.markdown("---")
tab1, tab2, tab3, tab4 = st.tabs(["👥 Users", "📝 Generation History", "🔍 Search", "⚙️ Admin Actions"])

# Tab 1: Users View
with tab1:
    st.markdown("### All Users")
    
    users_df = load_usage_data()
    
    if len(users_df) > 0:
        # Quick Actions
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            users_at_limit = len(users_df[users_df['usage_count'] >= 3])
            if st.button(f"🔄 Reset All Users at Limit ({users_at_limit})", key="bulk_reset", disabled=users_at_limit == 0):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE usage_tracking SET usage_count = 0 WHERE usage_count >= 3")
                cursor.execute("DELETE FROM generation_history WHERE user_hash IN (SELECT user_hash FROM usage_tracking WHERE usage_count >= 3)")
                conn.commit()
                conn.close()
                st.success(f"✅ Reset {users_at_limit} users!")
                st.rerun()
        
        with col_act2:
            if st.button("🔄 Reset ALL Users to 0", key="reset_all_users"):
                if st.session_state.get('confirm_reset_all', False):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE usage_tracking SET usage_count = 0")
                    cursor.execute("DELETE FROM generation_history")
                    conn.commit()
                    conn.close()
                    st.session_state.confirm_reset_all = False
                    st.success(f"✅ All users reset!")
                    st.rerun()
                else:
                    st.session_state.confirm_reset_all = True
                    st.warning("⚠️ Click again to confirm")
        
        st.markdown("---")
        
        # Display filters
        col1, col2 = st.columns(2)
        with col1:
            filter_limit = st.checkbox("Show only users at limit (3/3)", value=False)
        with col2:
            sort_by = st.selectbox("Sort by", ["Last Used", "First Used", "Usage Count"], key="sort_users")
        
        # Apply filters
        if filter_limit:
            users_df = users_df[users_df['usage_count'] >= 3]
        
        # Apply sorting
        if sort_by == "Last Used":
            users_df = users_df.sort_values('last_used', ascending=False)
        elif sort_by == "First Used":
            users_df = users_df.sort_values('first_used', ascending=False)
        else:
            users_df = users_df.sort_values('usage_count', ascending=False)
        
        # Display data with actions
        st.markdown(f"**Showing {len(users_df)} users**")
        
        for idx, row in users_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.markdown(f"**{row['ip_address'][:30]}**")
                    st.caption(f"Hash: {row['user_hash'][:16]}...")
                
                with col2:
                    st.markdown(f"Device: {row['device_info'][:40]}...")
                    st.caption(f"Last used: {row['last_used']}")
                
                with col3:
                    if row['usage_count'] >= 3:
                        st.error(f"🔴 {row['usage_count']}/3")
                    else:
                        st.success(f"✅ {row['usage_count']}/3")
                
                with col4:
                    if st.button("🔄", key=f"reset_{row['id']}", help="Reset this user"):
                        reset_user_count(row['user_hash'])
                        st.success("Reset!")
                        st.rerun()
                
                st.markdown("---")
        
        # Download button
        csv = users_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Users CSV",
            data=csv,
            file_name=f"users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No users in the database yet.")

# Tab 2: Generation History
with tab2:
    st.markdown("### Generation History")
    
    history_df = load_generation_history()
    
    if len(history_df) > 0:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            field_filter = st.multiselect(
                "Filter by Field",
                options=sorted(history_df['field'].unique()),
                key="field_filter"
            )
        with col2:
            difficulty_filter = st.multiselect(
                "Filter by Difficulty",
                options=sorted(history_df['difficulty_level'].unique()),
                key="difficulty_filter"
            )
        with col3:
            limit = st.slider("Show last N records", 10, 500, 50, key="history_limit")
        
        # Apply filters
        filtered_df = history_df
        if field_filter:
            filtered_df = filtered_df[filtered_df['field'].isin(field_filter)]
        if difficulty_filter:
            filtered_df = filtered_df[filtered_df['difficulty_level'].isin(difficulty_filter)]
        
        # Limit records
        filtered_df = filtered_df.head(limit)
        
        # Display
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "user_hash": st.column_config.TextColumn("User Hash", width="small"),
                "ip_address": st.column_config.TextColumn("IP", width="small"),
                "topic": st.column_config.TextColumn("Topic", width="medium"),
                "field": st.column_config.TextColumn("Field", width="small"),
                "difficulty_level": st.column_config.TextColumn("Level", width="small"),
                "generated_at": st.column_config.DatetimeColumn("Generated At", width="medium"),
            }
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download History CSV",
            data=csv,
            file_name=f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Analytics
        st.markdown("---")
        st.markdown("### 📈 Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top 5 Topics**")
            top_topics = history_df['topic'].value_counts().head(5)
            st.bar_chart(top_topics)
        
        with col2:
            st.markdown("**Top 5 Fields**")
            top_fields = history_df['field'].value_counts().head(5)
            st.bar_chart(top_fields)
    else:
        st.info("No generation history yet.")

# Tab 3: Search
with tab3:
    st.markdown("### 🔍 Search Database")
    
    search_type = st.radio("Search by", ["IP Address", "User Hash", "Topic"])
    search_query = st.text_input("Enter search term")
    
    if search_query:
        conn = get_connection()
        
        if search_type == "IP Address":
            query = "SELECT * FROM usage_tracking WHERE ip_address LIKE ?"
            df = pd.read_sql_query(query, conn, params=(f"%{search_query}%",))
            
            if len(df) > 0:
                st.markdown(f"**Found {len(df)} user(s)**")
                st.dataframe(df, use_container_width=True)
                
                # Quick actions for found users
                st.markdown("---")
                st.markdown("**Quick Actions**")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"🔄 Reset All {len(df)} Users", key="reset_search_ip"):
                        user_hashes = df['user_hash'].tolist()
                        count = reset_multiple_users(user_hashes)
                        st.success(f"✅ Reset {count} users!")
                        st.rerun()
                
                with col2:
                    if st.button(f"🗑️ Delete All {len(df)} Users", key="delete_search_ip"):
                        for user_hash in df['user_hash'].tolist():
                            delete_user(user_hash)
                        st.success(f"✅ Deleted {len(df)} users!")
                        st.rerun()
            else:
                st.info("No users found with that IP address.")
            
        elif search_type == "User Hash":
            # Get user info
            query = "SELECT * FROM usage_tracking WHERE user_hash LIKE ?"
            user_df = pd.read_sql_query(query, conn, params=(f"%{search_query}%",))
            
            if len(user_df) > 0:
                st.markdown("**User Information**")
                
                for idx, user in user_df.iterrows():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**IP:** {user['ip_address']}")
                        st.caption(f"Hash: {user['user_hash']}")
                        st.caption(f"Usage: {user['usage_count']}/3")
                    
                    with col2:
                        if st.button("🔄 Reset", key=f"reset_hash_{idx}"):
                            reset_user_count(user['user_hash'])
                            st.success("✅ Reset!")
                            st.rerun()
                    
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_hash_{idx}"):
                            delete_user(user['user_hash'])
                            st.success("✅ Deleted!")
                            st.rerun()
                    
                    st.markdown("---")
                
                # Get their history
                user_hash = user_df.iloc[0]['user_hash']
                query = "SELECT * FROM generation_history WHERE user_hash = ?"
                history_df = pd.read_sql_query(query, conn, params=(user_hash,))
                
                st.markdown(f"**Generation History ({len(history_df)} records)**")
                if len(history_df) > 0:
                    st.dataframe(history_df, use_container_width=True)
                else:
                    st.info("No generation history.")
            else:
                st.warning("No user found with that hash.")
                
        elif search_type == "Topic":
            query = """
                SELECT gh.*, ut.ip_address 
                FROM generation_history gh
                LEFT JOIN usage_tracking ut ON gh.user_hash = ut.user_hash
                WHERE gh.topic LIKE ?
            """
            df = pd.read_sql_query(query, conn, params=(f"%{search_query}%",))
            
            if len(df) > 0:
                st.markdown(f"**Found {len(df)} generations**")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No topics found matching your search.")
        
        conn.close()

# Tab 4: Admin Actions
with tab4:
    st.markdown("### ⚙️ Database Management")
    
    # Quick stats
    users_df = load_usage_data()
    total_users = len(users_df)
    users_at_limit = len(users_df[users_df['usage_count'] >= 3]) if total_users > 0 else 0
    users_active = len(users_df[users_df['usage_count'] > 0]) if total_users > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", total_users)
    with col2:
        st.metric("Users at Limit (3/3)", users_at_limit)
    with col3:
        st.metric("Active Users", users_active)
    
    st.markdown("---")
    st.warning("⚠️ **Warning**: These actions cannot be undone!")
    st.markdown("---")
    
    # Bulk Reset Options
    st.markdown("#### 🔄 Bulk Reset Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Reset by Usage Count**")
        min_usage = st.number_input("Reset users with usage >=", min_value=1, max_value=3, value=3)
        
        affected = len(users_df[users_df['usage_count'] >= min_usage]) if total_users > 0 else 0
        
        if st.button(f"🔄 Reset {affected} Users (>= {min_usage} uses)", disabled=affected == 0):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE usage_tracking SET usage_count = 0 WHERE usage_count >= {min_usage}")
            cursor.execute(f"DELETE FROM generation_history WHERE user_hash IN (SELECT user_hash FROM usage_tracking WHERE usage_count >= {min_usage})")
            conn.commit()
            conn.close()
            st.success(f"✅ Reset {affected} users!")
            st.rerun()
    
    with col2:
        st.markdown("**Reset Inactive Users**")
        days_inactive = st.number_input("Days inactive", min_value=1, max_value=365, value=30)
        
        if st.button(f"🔄 Reset Users Inactive > {days_inactive} days"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE usage_tracking 
                SET usage_count = 0 
                WHERE last_used < datetime('now', '-{days_inactive} days')
            """)
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            st.success(f"✅ Reset {affected} inactive users!")
            st.rerun()
    
    st.markdown("---")
    
    # Individual User Management
    st.markdown("#### 👤 Individual User Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Reset Specific User**")
        if len(users_df) > 0:
            # Create display options
            user_options = {}
            for _, row in users_df.iterrows():
                display = f"{row['ip_address'][:20]}... ({row['usage_count']}/3) - {row['user_hash'][:8]}..."
                user_options[display] = row['user_hash']
            
            selected_user = st.selectbox("Select user to reset", options=list(user_options.keys()))
            
            if st.button("🔄 Reset User Count to 0", type="secondary"):
                user_hash = user_options[selected_user]
                reset_user_count(user_hash)
                st.success(f"✅ User reset successfully!")
                st.rerun()
        else:
            st.info("No users to reset.")
    
    with col2:
        st.markdown("**Delete Specific User**")
        if len(users_df) > 0:
            selected_user_del = st.selectbox("Select user to delete", options=list(user_options.keys()), key="delete_user")
            
            if st.button("🗑️ Delete User Permanently", type="secondary"):
                user_hash = user_options[selected_user_del]
                delete_user(user_hash)
                st.success(f"✅ User deleted successfully!")
                st.rerun()
        else:
            st.info("No users to delete.")
    
    st.markdown("---")
    
    # Dangerous actions
    st.markdown("#### 🚨 Dangerous Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset ALL Users to 0", type="primary"):
            if 'confirm_bulk_reset' not in st.session_state:
                st.session_state.confirm_bulk_reset = False
            
            if st.session_state.confirm_bulk_reset:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE usage_tracking SET usage_count = 0")
                cursor.execute("DELETE FROM generation_history")
                conn.commit()
                conn.close()
                st.session_state.confirm_bulk_reset = False
                st.success(f"✅ All {total_users} users reset!")
                st.rerun()
            else:
                st.session_state.confirm_bulk_reset = True
                st.warning("⚠️ Click again to confirm!")
    
    with col2:
        if st.button("🗑️ Clear All Data (Delete Everything)", type="primary"):
            if 'confirm_delete_all' not in st.session_state:
                st.session_state.confirm_delete_all = False
            
            if st.session_state.confirm_delete_all:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM generation_history")
                cursor.execute("DELETE FROM usage_tracking")
                conn.commit()
                conn.close()
                st.session_state.confirm_delete_all = False
                st.success("✅ All data cleared!")
                st.rerun()
            else:
                st.session_state.confirm_delete_all = True
                st.warning("⚠️ Click again to confirm deletion of ALL data!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>🔐 Admin Dashboard | Theory2Practice AI Bridge</p>
    <p>Database: usage_tracking.db</p>
</div>
""", unsafe_allow_html=True)
