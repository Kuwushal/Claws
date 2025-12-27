# Google OAuth Setup Guide for Django with django-allauth

## Complete Setup Instructions

### 1. Dependencies Installed ✅
- django-allauth==0.57.0
- PyJWT==2.8.0
- cryptography==43.0.3

### 2. Settings Configuration ✅
Your `settings.py` is configured with:
- Google OAuth provider
- Proper authentication backends
- Email-based authentication
- Required middleware

### 3. URL Configuration ✅
Your `urls.py` includes allauth URLs at `/accounts/`

### 4. Templates Created ✅
- Login page with Google OAuth button
- Signup page with Google OAuth button
- Logout confirmation page

### 5. Navigation Updated ✅
Login/Logout links added to navigation menu

## Next Steps - Google Console Setup

### 1. Create Google OAuth Application

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `http://127.0.0.1:8000/accounts/google/login/callback/`
     - `http://localhost:8000/accounts/google/login/callback/`
   - Add authorized JavaScript origins:
     - `http://127.0.0.1:8000`
     - `http://localhost:8000`

### 2. Environment Variables Setup

Create a `.env` file in your project root:

```bash
# Copy from .env.example and fill in your values
cp .env.example .env
```

Add your Google OAuth credentials to `.env`:
```
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id-here
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret-here
```

### 3. Django Admin Setup

1. Create superuser:
```bash
python3 manage.py createsuperuser
```

2. Run the development server:
```bash
python3 manage.py runserver
```

3. Go to Django Admin at `http://127.0.0.1:8000/admin/`

4. Add Social Application:
   - Go to "Social Applications" under "Social Accounts"
   - Click "Add Social Application"
   - Provider: Google
   - Name: Google OAuth
   - Client ID: (from Google Console)
   - Secret Key: (from Google Console)
   - Sites: Select your site (example.com by default)

### 4. Test the Integration

1. Visit `http://127.0.0.1:8000/accounts/login/`
2. Click "Continue with Google"
3. Complete OAuth flow
4. You should be redirected back to your site and logged in

## Available URLs

- Login: `/accounts/login/`
- Signup: `/accounts/signup/`
- Logout: `/accounts/logout/`
- Google OAuth: `/accounts/google/login/`

## Troubleshooting

### Common Issues:

1. **"redirect_uri_mismatch" error**
   - Ensure redirect URI in Google Console matches exactly: `http://127.0.0.1:8000/accounts/google/login/callback/`

2. **"Social application not found" error**
   - Make sure you've added the Social Application in Django Admin
   - Verify the Client ID and Secret are correct

3. **"Site matching query does not exist" error**
   - Go to Django Admin > Sites
   - Update the default site domain to `127.0.0.1:8000` or your domain

### Production Setup:

For production, update:
1. Google Console authorized origins and redirect URIs with your production domain
2. Django `ALLOWED_HOSTS` setting
3. Environment variables on your production server

## Security Notes

- Never commit `.env` file to version control
- Use HTTPS in production
- Regularly rotate OAuth secrets
- Review OAuth scopes and permissions