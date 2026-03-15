# Admin Dashboard Authentication

The admin dashboard is protected with username/password authentication to prevent public access.

## Setting Up Admin Credentials

### Method 1: Using .env file (Recommended)

1. Open the `.env` file in your project root
2. Update the `ADMIN_USERNAME` to your desired username
3. Generate a password hash using:
   ```bash
   python -c "import hashlib; print(hashlib.sha256('YOUR_NEW_PASSWORD'.encode()).hexdigest())"
   ```
4. Update `ADMIN_PASSWORD_HASH` with the generated hash
5. Save the file and restart the app

### Method 2: Using Environment Variables

Set these environment variables in your deployment platform (e.g., Streamlit Cloud):

```
ADMIN_USERNAME=your_username
ADMIN_PASSWORD_HASH=your_password_hash
```

## Deployment Security

When deploying to Streamlit Cloud or other platforms:

1. **Add credentials to Secrets**:
   - Go to your app settings
   - Add `ADMIN_USERNAME` and `ADMIN_PASSWORD_HASH` to secrets
   - Do NOT commit `.env` file with real credentials to Git

2. **Update .gitignore**:
   - Ensure `.env` is in `.gitignore` (already included)

3. **Use Strong Passwords**:
   - At least 12 characters
   - Mix of uppercase, lowercase, numbers, and symbols

## How It Works

- The dashboard checks authentication on every page load
- Login state is stored in Streamlit session state
- Passwords are hashed using SHA-256 before comparison
- No plain-text passwords are stored anywhere

## Logout

Click the "🚪 Logout" button in the sidebar to end your session.
