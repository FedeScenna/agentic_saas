from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from supabase import create_client, Client
import os
from datetime import datetime
import uuid
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'your-supabase-url')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'your-supabase-key')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup page"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Create user with Supabase and set redirect URL
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "email_redirect_to": f"{request.url_root}auth/callback"
                }
            })
            
            if response.user:
                flash('Account created successfully! Please check your email to verify your account.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error creating account. Please try again.', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Sign in with Supabase
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                session['user'] = {
                    'id': response.user.id,
                    'email': response.user.email
                }
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials. Please try again.', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', user=session['user'])

@app.route('/chat')
def chat():
    """Chat interface"""
    if 'user' not in session:
        flash('Please log in to access the chat.', 'error')
        return redirect(url_for('login'))
    
    return render_template('chat.html', user=session['user'])

@app.route('/auth/google')
def google_auth():
    """Initiate Google OAuth sign-in"""
    try:
        # Get the Google OAuth URL from Supabase
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": f"{request.url_root}auth/callback"
            }
        })
        
        if response.url:
            return redirect(response.url)
        else:
            flash('Error initiating Google sign-in. Please try again.', 'error')
            return redirect(url_for('login'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/auth/callback')
def auth_callback():
    """Handle OAuth and email confirmation callbacks"""
    # Get the URL parameters
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        flash(f'Authentication error: {error}', 'error')
        return redirect(url_for('login'))
    
    if code:
        try:
            # Exchange the code for a session
            response = supabase.auth.exchange_code_for_session({
                "auth_code": code
            })
            
            if response.user:
                session['user'] = {
                    'id': response.user.id,
                    'email': response.user.email
                }
                flash('Successfully signed in!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Error completing authentication. Please try again.', 'error')
                return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('login'))
    
    # If no code, just redirect to login
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for chat functionality"""
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    message = data.get('message', '')
    
    # Here you would integrate with your data processing and AI chat logic
    # For now, returning a simple response
    response = {
        'message': f"I received your message: '{message}'. This is where your AI chat with your data would happen!",
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
