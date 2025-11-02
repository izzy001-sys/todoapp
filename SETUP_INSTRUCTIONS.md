# Setup and Installation Instructions

## Prerequisites

1. Python 3.11 or higher
2. Virtual environment (venv) already exists in the project folder
3. Git (for CI/CD with GitHub Actions)

## Step-by-Step Installation

### 1. Activate Virtual Environment

**Windows:**
```powershell
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn (web framework and server)
- SQLAlchemy (ORM for database)
- Python-Jose (JWT authentication)
- Passlib (password hashing)
- Jinja2 (templating)
- Pytest and related testing libraries
- Playwright (for E2E testing)

### 3. Install Playwright Browsers

For running end-to-end tests:

```bash
playwright install chromium
```

Or install all browsers:
```bash
playwright install
```

## Running the Application

### Start the Development Server

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables auto-reload on code changes.

### Access the Application

- **Web Interface:** http://localhost:8000
- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative API Docs (ReDoc):** http://localhost:8000/redoc

## Testing

### Run Unit Tests

```bash
pytest tests/test_services.py tests/test_routes.py -v
```

### Run E2E Tests

**Terminal 1 - Start the server:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Run Playwright tests:**
```bash
pytest tests/test_e2e.py -v
```

### Run All Tests

```bash
pytest -v
```

## Database

The SQLite database (`todo_app.db`) is automatically created when you first run the application. The database schema is defined in `app/models.py` and initialized in `app/database.py`.

To reset the database, simply delete `todo_app.db` and restart the application.

## Continuous Integration Setup

### GitHub Actions Setup

1. **Create a GitHub repository:**
   - Go to GitHub and create a new repository
   - Don't initialize with README (if you already have code)

2. **Connect your local repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **GitHub Actions will automatically run:**
   - On every push to main/master/develop branches
   - On every pull request to these branches

The CI workflow (`.github/workflows/ci.yml`) will:
- Install dependencies
- Install Playwright browsers
- Run unit tests
- Start the server
- Run E2E tests

## Environment Configuration

### Production Security

**Important:** Before deploying to production, change the `SECRET_KEY` in `app/auth.py`:

```python
SECRET_KEY = "your-very-secure-random-key-here"
```

Generate a secure key using:
```python
import secrets
print(secrets.token_urlsafe(32))
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:
```bash
uvicorn app.main:app --reload --port 8001
```

### Database Issues

If you encounter database errors:
1. Delete `todo_app.db`
2. Restart the application

### Playwright Installation Issues

If Playwright browsers fail to install:
```bash
playwright install chromium --force
```

### Import Errors

Make sure you're in the project root directory and the virtual environment is activated.

## Project Structure Overview

```
appexample03/
├── app/                    # Application code
│   ├── main.py            # FastAPI app entry point
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── auth.py            # Authentication logic
│   ├── services.py        # Business logic
│   └── routers/           # API routes
├── tests/                  # Test files
├── templates/              # HTML templates
├── static/                 # CSS and JavaScript
│   ├── css/
│   └── js/
├── .github/
│   └── workflows/         # CI/CD configuration
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Next Steps

1. ✅ Activate virtual environment
2. ✅ Install dependencies
3. ✅ Start the server
4. ✅ Open http://localhost:8000 in your browser
5. ✅ Sign up for an account
6. ✅ Create your first todo!

## Support

For issues or questions:
1. Check the README.md for API documentation
2. Review test files for usage examples
3. Check FastAPI documentation: https://fastapi.tiangolo.com/

