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

3. **Install Playwright browsers (for E2E tests):**
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

For production, make sure to change the `SECRET_KEY` in `app/auth.py` to a secure random string.

## License

MIT

