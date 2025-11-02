# Step-by-Step Guide to Running Tests

## Prerequisites Check

Before running tests, make sure:
1. ✅ Virtual environment is activated
2. ✅ All dependencies are installed: `pip install -r requirements.txt`
3. ✅ Playwright browsers are installed: `playwright install chromium`

## Types of Tests

Your test suite has **3 test files**:

1. **`test_services.py`** - Unit tests for business logic (services layer)
2. **`test_routes.py`** - API endpoint tests (uses FastAPI TestClient)
3. **`test_e2e.py`** - End-to-end browser tests (uses Playwright)

---

## Option 1: Run Unit Tests (No Server Needed)

These tests don't require the server to be running. They use database fixtures.

### Step 1: Open a new terminal/command prompt

Keep your server running in the first terminal, and open a **new terminal** for tests.

### Step 2: Activate virtual environment (if not already active)

**Windows:**
```powershell
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Navigate to project directory

```bash
cd c:\Users\debo_\Desktop\Crewai\appexample03
```

### Step 4: Run service tests

```bash
pytest tests/test_services.py -v
```

**Expected output:** Should show tests passing with details.

### Step 5: Run route tests

```bash
pytest tests/test_routes.py -v
```

**Expected output:** Should show tests passing with details.

### Step 6: Run both unit tests together

```bash
pytest tests/test_services.py tests/test_routes.py -v
```

---

## Option 2: Run All Tests (Including E2E)

### Important Note for E2E Tests

Your E2E tests are configured to use `http://localhost:8000`, but your server is running on `http://127.0.0.1:8000`. 

**Both should work** (localhost usually resolves to 127.0.0.1), but if you encounter connection issues, you have two options:

**Option A:** Keep server running on `127.0.0.1:8000` and update the test (recommended)
**Option B:** Start server with `localhost` instead:
```bash
uvicorn app.main:app --reload --host localhost
```

### Step 1: Ensure server is running

In your **first terminal**, make sure the server is running:
```bash
uvicorn app.main:app --reload
```

The server should be accessible at `http://127.0.0.1:8000` or `http://localhost:8000`

### Step 2: Open a new terminal for tests

Open a **new terminal/command prompt** (keep the server running in the first terminal).

### Step 3: Activate virtual environment

**Windows:**
```powershell
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Navigate to project directory

```bash
cd c:\Users\debo_\Desktop\Crewai\appexample03
```

### Step 5: Run E2E tests

```bash
pytest tests/test_e2e.py -v
```

**Note:** These tests will open a browser (Chromium) automatically. The browser might appear briefly - this is normal.

**Expected output:** Should show E2E tests passing.

### Step 6: Run all tests together

```bash
pytest tests/ -v
```

This runs all tests in the `tests/` directory.

---

## Option 3: Run Specific Tests

### Run a single test function

```bash
pytest tests/test_services.py::test_create_user -v
```

### Run tests matching a pattern

```bash
pytest tests/ -k "todo" -v
```

This runs all tests with "todo" in their name.

---

## Common Test Commands

### Verbose output (shows more details)

```bash
pytest tests/ -v
```

### Very verbose (shows print statements)

```bash
pytest tests/ -vv -s
```

### Show test coverage (if coverage is installed)

```bash
pytest tests/ --cov=app --cov-report=html
```

### Stop on first failure

```bash
pytest tests/ -x
```

### Run tests in parallel (faster)

```bash
pip install pytest-xdist
pytest tests/ -n auto
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError" or import errors

**Solution:** Make sure you're in the project root directory and virtual environment is activated.

```bash
# Check you're in the right directory
cd c:\Users\debo_\Desktop\Crewai\appexample03

# Activate venv
.\venv\Scripts\activate

# Verify Python path
python -c "import sys; print(sys.path)"
```

### Issue: Playwright browser not found

**Solution:** Install Playwright browsers

```bash
playwright install chromium
```

### Issue: E2E tests can't connect to server

**Solution 1:** Make sure server is running on the correct host

```bash
# In first terminal, restart server with:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Solution 2:** Update test file to use `127.0.0.1` instead of `localhost` (see below)

### Issue: Database locked errors

**Solution:** Unit tests create their own test database. If you see database errors, make sure:
- No other process is using the test database
- Tests are not running in parallel without proper setup

---

## Quick Reference

| Test Type | Command | Server Needed? |
|-----------|---------|----------------|
| Service tests | `pytest tests/test_services.py -v` | ❌ No |
| Route tests | `pytest tests/test_routes.py -v` | ❌ No |
| E2E tests | `pytest tests/test_e2e.py -v` | ✅ Yes |
| All tests | `pytest tests/ -v` | ✅ Yes (for E2E) |

---

## Expected Test Results

After running tests, you should see output like:

```
tests/test_services.py::test_create_user PASSED
tests/test_services.py::test_create_user_duplicate_username PASSED
tests/test_routes.py::test_signup PASSED
tests/test_e2e.py::test_signup_and_create_todo PASSED

========================== X passed in Y.YYs ==========================
```

All tests should pass if everything is set up correctly!

