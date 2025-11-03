import os, sys, time, socket, subprocess, urllib.request
import pytest

def _find_free_port() -> int:
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port

def _wait_for(url: str, timeout: float = 10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url):
                return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Server did not start at {url} within {timeout}s")

@pytest.fixture(scope="session", autouse=True)
def live_server():
    port = _find_free_port()
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
def app_base_url(live_server):
    return live_server

# IMPORTANT: alias required by pytest-playwright and your tests
@pytest.fixture(scope="session")
def base_url(app_base_url):
    return app_base_url
