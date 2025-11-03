# tests/conftest.py
import os, sys, time, socket, subprocess, urllib.request
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.database import Base, get_db
from app.main import app

# -------------------------- DB / API client (unit/integration) --------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todo_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class NoRedirectClient(TestClient):
    # Make sure tests see 303 instead of following to 200
    def request(self, *args, **kwargs):
        kwargs.setdefault("allow_redirects", False)
        return super().request(*args, **kwargs)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield NoRedirectClient(app)
    finally:
        app.dependency_overrides.clear()

# -------------------------- Live server for Playwright e2e --------------------------

def _free_port() -> int:
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port

def _wait_for(url: str, timeout: float = 15.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url):
                return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Server did not start at {url} within {timeout}s")

@pytest.fixture(scope="session", autouse=True)
def _uvicorn_server():
    """
    Start uvicorn once for the e2e session.
    API tests use TestClient and are unaffected.
    """
    port = _free_port()
    base = f"http://127.0.0.1:{port}"
    env = os.environ.copy()
    env["APP_ENV"] = "test"

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app",
         "--host", "127.0.0.1", "--port", str(port)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    _wait_for(base)
    try:
        yield base
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()

@pytest.fixture(scope="session")
def base_url(_uvicorn_server):
    """Fixture name that pytest-playwright expects."""
    return _uvicorn_server

# -------------------------- Optional: Playwright launch tweaks --------------------------

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    # keep your headless setting
    return {**browser_type_launch_args, "headless": True}

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # keep your viewport setting
    return {**browser_context_args, "viewport": {"width": 1920, "height": 1080}}
