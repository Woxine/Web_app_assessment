# Farmer's Delight Wiki

Flask-based encyclopedia web application for the Minecraft mod "Farmer's Delight".

## Features

- ✅ Browse crop and meal information (paginated display)
- ✅ Search functionality (supports keyword search and multiple sorting options)
- ✅ User registration/login system (password encryption)
- ✅ AJAX like functionality (no-refresh interaction)
- ✅ Rankings (based on like count)
- ✅ Flask-Admin backend management
- ✅ Responsive design (WCAG compatible)
- ✅ Security measures (SQL injection, XSS, CSRF protection)
- ✅ Logging system

## Tech Stack

- **Backend**: Python 3 + Flask
- **Database**: Flask-SQLAlchemy (SQLite, supports MySQL)
- **Frontend**: Jinja2 + HTML5 + CSS3
- **Forms**: Flask-WTF (CSRF protection)
- **Authentication**: Flask-Login
- **Management**: Flask-Admin
- **Migration**: Flask-Migrate

## Installation Steps

### 1. Clone the project

```bash
git clone <repository-url>
cd cw2
```

### 2. Create virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `instance/config.py` file:

```python
SECRET_KEY = 'your-secret-key-here'
DATABASE_URL = 'sqlite:///app.db'  # Default uses SQLite
# To use MySQL, uncomment and modify the following line:
# DATABASE_URL = 'mysql://user:password@localhost/farmers_delight'
```

### 5. Initialize database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the application

```bash
python run.py
```

Visit http://localhost:5000

## Database Models

### Core Models

- **User**: User table (id, username, email, password_hash)
- **Crop**: Crop table (id, name, description, image_url, hunger_points)
- **Meal**: Meal table (id, name, description, image_url, hunger_restored, saturation)

### Many-to-Many Relationships

1. **meal_ingredients**: Meal ↔ Crop (meal-ingredient relationship)
2. **user_likes_crops**: User ↔ Crop (user likes crops)
3. **user_likes_meals**: User ↔ Meal (user likes meals)

## Form Control Types

Meets at least 5 form control requirements:

1. Text input (TextInput)
2. Password input (PasswordField)
3. Submit button (SubmitField)
4. Dropdown list (SelectField)
5. Radio button (RadioField)
6. Checkbox (BooleanField)
7. Text area (TextAreaField)

## Running Tests

```bash
python -m pytest tests/
# or
python -m unittest discover tests
```

## Deploy to PythonAnywhere

1. Upload project files to PythonAnywhere
2. Configure WSGI file (refer to `wsgi.py`)
3. Set environment variables (SECRET_KEY, DATABASE_URL optional, defaults to SQLite)
4. Run database migrations
5. Configure static file paths

## Security Measures

- ✅ SQL Injection Protection: Using SQLAlchemy ORM
- ✅ XSS Protection: Jinja2 auto-escaping
- ✅ CSRF Protection: Flask-WTF CSRF Token
- ✅ Password Encryption: Werkzeug security

## Accessibility

- ✅ Semantic HTML5 (nav, main, article, footer)
- ✅ ARIA labels (aria-label, aria-describedby)
- ✅ Color contrast meets WCAG AA level standards

## Project Structure

```
cw2/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── models.py            # Data models
│   ├── forms.py             # Flask-WTF forms
│   ├── views.py             # Main view routes
│   ├── auth.py              # Authentication routes
│   ├── admin.py             # Flask-Admin configuration
│   ├── utils.py             # Utility functions
│   ├── static/              # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/           # Jinja2 templates
├── tests/                   # Unit tests
├── migrations/              # Database migrations
├── instance/                # Instance configuration
├── logs/                    # Log files
├── config.py                # Configuration file
├── run.py                   # Application entry point
├── wsgi.py                  # WSGI configuration
└── requirements.txt         # Dependency list
```

## License

This project is a coursework project.

## Author

Leeds University - XJCO2011 Web Application Development

