# Business Insights SaaS Platform

A Flask-based SaaS platform that offers local agent products for business data analysis and reporting.

## Features

- User authentication and account management
- Dashboard for monitoring data analysis tasks
- Local agent deployment and management
- Report generation and visualization
- Subscription management

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment and activate it:
```
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables:
```
# Create a .env file with the following variables
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///app.db
```

5. Initialize the database:
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running the Application

```
flask run
```

The application will be available at http://127.0.0.1:5000/

## Development

- `app/` - Main application package
  - `models/` - Database models
  - `routes/` - Route handlers
  - `static/` - Static assets (CSS, JS, images)
  - `templates/` - Jinja2 templates
  - `__init__.py` - Application factory
  - `config.py` - Configuration settings

## License

[MIT License](LICENSE) 