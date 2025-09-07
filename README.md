<<<<<<< HEAD
# DataChat - Chat with Your Data

A Flask-based web application that allows users to chat with their own unstructured and structured data using AI. Built with a modern dark mode interface and Supabase authentication.

## Features

- 🔐 **Secure Authentication** - User signup and login with Supabase
- 🎨 **Modern Dark Mode UI** - Beautiful, responsive interface
- 💬 **AI Chat Interface** - Chat with your data using natural language
- 📊 **Data Source Management** - Connect multiple data sources
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🚀 **Simple Setup** - Easy to deploy and configure

## Screenshots

The application features:
- Landing page with hero section, features, and pricing
- User authentication (signup/login)
- Dashboard with data source management
- Interactive chat interface
- Dark mode theme throughout

## Prerequisites

- Python 3.8 or higher
- Supabase account and project
- Git

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd agentic_saas
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Supabase**
   - Go to [Supabase](https://supabase.com) and create a new project
   - Go to Settings > API to get your project URL and anon key
   - Copy `env_example.txt` to `.env` and fill in your credentials:
     ```bash
     cp env_example.txt .env
     ```

5. **Configure environment variables**
   Edit the `.env` file with your actual values:
   ```
   SECRET_KEY=your-secret-key-here
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-supabase-anon-key
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

## Project Structure

```
agentic_saas/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── env_example.txt       # Environment variables template
├── README.md             # This file
├── Rules.md              # Project requirements
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── index.html        # Landing page
    ├── signup.html       # User registration
    ├── login.html        # User login
    ├── dashboard.html    # User dashboard
    └── chat.html         # Chat interface
```

## Usage

1. **Sign Up**: Create a new account using the signup page
2. **Login**: Sign in with your credentials
3. **Dashboard**: View your data sources and recent conversations
4. **Chat**: Start chatting with your data using natural language

## Configuration

### Supabase Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to Authentication > Settings and configure:
   - Site URL: `http://localhost:5000` (for development)
   - Redirect URLs: `http://localhost:5000/dashboard`
3. Get your project URL and anon key from Settings > API

### Environment Variables

- `SECRET_KEY`: Flask secret key for session management
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anonymous key

## Development

### Adding New Features

1. **New Routes**: Add routes in `app.py`
2. **New Templates**: Create HTML files in `templates/`
3. **Styling**: Modify the CSS in `base.html` or add new stylesheets

### Database Integration

The current setup uses Supabase for authentication. To add data storage:

1. Create tables in your Supabase project
2. Use the Supabase client in your Flask routes
3. Add data models and CRUD operations

## Deployment

### Heroku

1. Create a `Procfile`:
   ```
   web: python app.py
   ```

2. Set environment variables in Heroku dashboard

3. Deploy:
   ```bash
   git push heroku main
   ```

### Other Platforms

The application can be deployed to any platform that supports Python/Flask:
- Railway
- Render
- DigitalOcean App Platform
- AWS Elastic Beanstalk

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, email your-email@example.com or create an issue in the repository.

## Roadmap

- [ ] File upload functionality
- [ ] Multiple data source connectors
- [ ] Advanced AI chat features
- [ ] User management dashboard
- [ ] API endpoints for external integrations
- [ ] Real-time chat updates
- [ ] Data visualization features
