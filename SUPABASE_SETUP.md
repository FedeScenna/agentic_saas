# Supabase Configuration for Google OAuth & Email Confirmation

## 🔧 Supabase Dashboard Configuration

### 1. Enable Google OAuth Provider

1. **Go to your Supabase Dashboard**
   - Visit: https://supabase.com/dashboard
   - Select your project

2. **Navigate to Authentication > Providers**
   - Click on "Authentication" in the left sidebar
   - Click on "Providers" tab

3. **Enable Google Provider**
   - Find "Google" in the list of providers
   - Toggle it to "Enabled"
   - You'll need to configure Google OAuth credentials (see Google Console setup below)

### 2. Configure Site URL and Redirect URLs

1. **Go to Authentication > URL Configuration**
   - Site URL: `http://localhost:5000` (for development)
   - Redirect URLs: Add these URLs:
     ```
     http://localhost:5000/auth/callback
     http://localhost:5000/dashboard
     ```

2. **For Production** (when you deploy):
   - Site URL: `https://yourdomain.com`
   - Redirect URLs: Add these URLs:
     ```
     https://yourdomain.com/auth/callback
     https://yourdomain.com/dashboard
     ```

### 3. Email Configuration

1. **Go to Authentication > Email Templates**
   - Customize the "Confirm signup" template
   - The confirmation link will now redirect to: `{{ .SiteURL }}/auth/callback`

2. **Email Settings**
   - Go to Authentication > Settings
   - Enable "Enable email confirmations"
   - Set "Email confirmation URL" to: `{{ .SiteURL }}/auth/callback`

## 🔑 Google Console Setup

### 1. Create Google OAuth Credentials

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Create a new project or select existing one

2. **Enable Google+ API**
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Application type: "Web application"
   - Name: "DataChat OAuth"

4. **Configure Authorized URLs**
   - Authorized JavaScript origins:
     ```
     http://localhost:5000
     https://yourdomain.com (for production)
     ```
   - Authorized redirect URIs:
     ```
     https://xpyuaozynvipeasiqrjh.supabase.co/auth/v1/callback
     ```

### 2. Get Google OAuth Credentials

1. **Copy the credentials**
   - Client ID: `your-google-client-id`
   - Client Secret: `your-google-client-secret`

2. **Add to Supabase**
   - Go back to Supabase Dashboard > Authentication > Providers
   - Click on Google provider
   - Enter your Google Client ID and Client Secret
   - Save the configuration

## 🔧 Environment Variables

Update your `.env` file with the correct Supabase URL:

```env
# Flask Configuration
SECRET_KEY='\x89\x1a\x97\xe0\xb7\x06PPn\x11<R'

# Supabase Configuration
SUPABASE_URL="https://xpyuaozynvipeasiqrjh.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhweXVhb3p5bnZpcGVhc2lxcmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcyNjM0NjEsImV4cCI6MjA3MjgzOTQ2MX0.0znbNo5JGN365WibBDoWZHTdrhqnB3ju5pxd2kGQyLk"
```

**Note**: Remove the trailing slash from SUPABASE_URL if present.

## 🧪 Testing the Setup

### 1. Test Email Signup
1. Go to `http://localhost:5000/signup`
2. Create an account with email/password
3. Check your email for confirmation link
4. Click the link - it should redirect to your app and log you in

### 2. Test Google OAuth
1. Go to `http://localhost:5000/login`
2. Click "Continue with Google"
3. Complete Google OAuth flow
4. Should redirect back to your dashboard

## 🚨 Troubleshooting

### Email Confirmation Links Not Working
- ✅ **Fixed**: Updated signup to include `email_redirect_to` parameter
- ✅ **Fixed**: Added `/auth/callback` route to handle email confirmations
- ✅ **Fixed**: Configured Supabase redirect URLs

### Google OAuth Not Working
- Check Google Console redirect URIs match Supabase callback URL
- Verify Google Client ID/Secret are correctly entered in Supabase
- Ensure Google+ API is enabled in Google Console

### Common Issues
1. **"Invalid redirect URI"**: Check Google Console redirect URIs
2. **"Client ID not found"**: Verify credentials in Supabase dashboard
3. **"Email confirmation failed"**: Check Supabase email settings and redirect URLs

## 📱 Production Deployment

When deploying to production:

1. **Update Supabase URLs**:
   - Site URL: `https://yourdomain.com`
   - Redirect URLs: `https://yourdomain.com/auth/callback`

2. **Update Google Console**:
   - Add production domain to authorized origins
   - Update redirect URIs if needed

3. **Update Environment Variables**:
   - Set production Supabase URL
   - Update any hardcoded localhost URLs
