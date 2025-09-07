# Setup Instructions for DataChat

## Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 for Windows
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Complete the installation

## Step 2: Verify Python Installation
Open a new PowerShell window and run:
```bash
python --version
```
You should see something like: `Python 3.11.x`

## Step 3: Install Dependencies
Navigate to your project folder and run:
```bash
pip install -r requirements.txt
```

## Step 4: Run the Application
```bash
python app.py
```

## Step 5: Access the Website
Open your browser and go to: `http://localhost:5000`

## Available URLs:
- **Home**: http://localhost:5000/
- **Signup**: http://localhost:5000/signup
- **Login**: http://localhost:5000/login
- **Dashboard**: http://localhost:5000/dashboard (after login)
- **Chat**: http://localhost:5000/chat (after login)

## Troubleshooting:
- If you get "Python not found", make sure Python is added to PATH
- If you get Supabase errors, check that your .env file has correct credentials
- If port 5000 is busy, the app will show an error with the correct port to use
