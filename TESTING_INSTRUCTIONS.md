# Step-by-Step Testing Instructions

## Prerequisites
- ✅ Your app is running on http://127.0.0.1:8000
- ✅ Virtual environment is activated
- ✅ All dependencies installed (`pip install -r requirements.txt`)
- ✅ Playwright browsers installed (`playwright install chromium`)

## Test Types

You have three test files:
1. **Unit Tests** (`test_services.py`) - Tests business logic (no server needed)
2. **Route Tests** (`test_routes.py`) - Tests API endpoints (no server needed, uses test client)
3. **E2E Tests** (`test_e2e.py`) - Tests full browser workflow (server must be running)

---

## Option 1: Run All Tests (Recommended)

This will run all tests in sequence.

### Steps:
1. **Keep your server running** (http://127.0.0.1:8000) - needed for E2E tests
2. **Open a new terminal/command prompt** (keep the server running in the first terminal)
3. **Navigate to project directory:**
   ```bash
   cd c:\Users\debo_\Desktop\Crewai\appexample03
   ```
4. **Activate virtual environment:**
   ```bash
   .\venv\Scripts\activate
   ```
5. **Run all tests:**
   ```bash
   pytest -v
   ```

---

## Option 2: Run Tests Separately

### A. Run Unit Tests Only (Service Layer)

These tests don't require the server to be running.

**Steps:**
1. Open terminal in project directory
2. Activate virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
3. Run service tests:
   ```bash
   pytest tests/test_services.py -v
   ```

**Expected output:** Tests for user creation, authentication, and todo CRUD operations.

---

### B. Run Route Tests Only (API Endpoints)

These tests use a test client and don't require the server to be running.

**Steps:**
1. Open terminal in project directory
2. Activate virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
3. Run route tests:
   ```bash
   pytest tests/test_routes.py -v
   ```

**Expected output:** Tests for signup, login, and todo API endpoints.

---

### C. Run E2E Tests Only (Browser Tests)

**⚠️ Important:** Your server must be running on http://127.0.0.1:8000

**Steps:**
1. **Keep your server running** in the first terminal
2. **Open a new terminal** in project directory
3. Activate virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
4. Run E2E tests:
   ```bash
   pytest tests/test_e2e.py -v
   ```

**Expected output:** Playwright will open Chrome, test signup, login, and todo interactions.

---

## Option 3: Run Specific Test Functions

### Run a single test function:
```bash
pytest tests/test_services.py::test_create_user -v
```

### Run tests matching a pattern:
```bash
pytest -k "test_create" -v
```

---

## Common Test Commands

### Verbose output (recommended):
```bash
pytest -v
```

### Very verbose output (shows print statements):
```bash
pytest -vv -s
```

### Run tests with coverage report:
```bash
pytest --cov=app --cov-report=html
```

### Run tests and stop on first failure:
```bash
pytest -x
```

### Run tests in parallel (faster):
```bash
pip install pytest-xdist
pytest -n auto
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError" or import errors
**Solution:** Make sure virtual environment is activated and you're in the project root directory.

### Issue: E2E tests fail with connection errors
**Solution:** 
- Verify server is running: `curl http://127.0.0.1:8000` or open in browser
- Check the URL in `tests/test_e2e.py` matches your server URL
- If your server is on a different port, update `base_url` in `test_e2e.py`

### Issue: Playwright browser not found
**Solution:**
```bash
playwright install chromium
```

### Issue: Database errors in tests
**Solution:** Tests use a separate test database (`test_todo_app.db`). If issues persist, delete this file and rerun tests.

### Issue: Tests timeout
**Solution:** E2E tests may take longer. Add timeout:
```bash
pytest tests/test_e2e.py -v --timeout=300
```

---

## Quick Test Workflow

**Terminal 1 (Server):**
```bash
cd c:\Users\debo_\Desktop\Crewai\appexample03
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 (Tests):**
```bash
cd c:\Users\debo_\Desktop\Crewai\appexample03
.\venv\Scripts\activate

# Run unit and route tests (no server needed)
pytest tests/test_services.py tests/test_routes.py -v

# Then run E2E tests (server must be running)
pytest tests/test_e2e.py -v
```

---

## Expected Test Results

### Successful Run:
```
tests/test_services.py::test_create_user PASSED
tests/test_services.py::test_authenticate_user PASSED
...
tests/test_routes.py::test_signup PASSED
...
tests/test_e2e.py::test_signup_and_create_todo PASSED
...

================== X passed in Y.YYs ==================
```

### If tests fail:
- Read the error message
- Check if the server is running (for E2E tests)
- Verify all dependencies are installed
- Check the troubleshooting section above

