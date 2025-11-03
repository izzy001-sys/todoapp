# Todo App

A full-stack todo application built with FastAPI, SQLAlchemy, and vanilla JavaScript.

## Features

- User authentication (signup, login, logout)
- CRUD operations for todos
- Server-rendered HTML templates
- RESTful API endpoints
- SQLite database with SQLAlchemy ORM
- Unit tests and E2E tests with Playwright

## Project Structure

```
appexample03/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── services.py          # Business logic
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       └── todos.py         # Todo routes
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   ├── test_services.py     # Service layer tests
│   ├── test_routes.py       # API route tests
│   └── test_e2e.py          # End-to-end tests
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── login.html           # Login page
│   └── signup.html          # Signup page
├── static/
│   ├── css/
│   │   └── style.css        # Styles
│   └── js/
│       └── app.js           # Frontend JavaScript
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI
├── requirements.txt
├── pytest.ini
└── README.md
```

## Installation

1. **Activate the virtual environment:**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env file with your configuration
   # IMPORTANT: Change SECRET_KEY to a secure random string for production
   ```

4. **Install Playwright browsers (for E2E tests):**
   ```bash
   playwright install chromium
   ```

## Running the Application

1. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the application:**
   - Open your browser and navigate to `http://localhost:8000`
   - The API documentation is available at `http://localhost:8000/docs`

## Docker Deployment

### Quick Start with Docker

**Prerequisites:** Docker and Docker Compose installed

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Run in background:**
   ```bash
   docker-compose up -d
   ```

3. **Stop the application:**
   ```bash
   docker-compose down
   ```

4. **Access the application:**
   - Web App: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

**For detailed Docker deployment instructions, see:**
- [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) - Complete deployment guide
- [README_DOCKER.md](README_DOCKER.md) - Quick reference commands

### Production Considerations

- Set a secure `SECRET_KEY` environment variable
- Database is persisted in `./data` directory
- For production, consider using PostgreSQL or MySQL
- Use a reverse proxy (nginx) with SSL certificates

## Testing

### Run unit tests:
```bash
pytest tests/test_services.py tests/test_routes.py -v
```

### Run E2E tests:
1. Start the server in one terminal:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. Run Playwright tests in another terminal:
   ```bash
   pytest tests/test_e2e.py -v
   ```

### Run all tests:
```bash
pytest -v
```

## API Endpoints

### Authentication
- `GET /signup` - Signup page
- `POST /signup` - Create new user
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /logout` - Logout user

### Todos
- `GET /` - Home page with todos
- `GET /todos` - Get all todos (requires authentication)
- `POST /todos` - Create a todo (requires authentication)
- `GET /todos/{todo_id}` - Get a specific todo (requires authentication)
- `PUT /todos/{todo_id}` - Update a todo (requires authentication)
- `DELETE /todos/{todo_id}` - Delete a todo (requires authentication)

## Continuous Integration

The project includes GitHub Actions workflow that runs on every push and pull request:
- Installs dependencies
- Runs unit tests
- Runs E2E tests with Playwright

## Database

The application uses SQLite database (`todo_app.db`). The database is automatically created when you first run the application. Tables are created using SQLAlchemy models.

## Environment Variables

The application uses environment variables for configuration. All settings are defined in the `.env` file.

### Setup

1. Copy `env.example` to `.env`:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` file with your configuration values

### Important Variables

- **SECRET_KEY**: JWT secret key - **Must be changed in production!**
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

- **SQLALCHEMY_DATABASE_URL**: Database connection string
- **CORS_ORIGINS**: Allowed CORS origins (comma-separated)

### Available Configuration

See `env.example` for all available configuration options including:
- Security settings (JWT, cookies)
- Database configuration
- CORS settings
- Application settings

**Never commit the `.env` file to version control!**

## License

MIT

