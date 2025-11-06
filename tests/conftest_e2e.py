# tests/conftest_e2e.py
import os, sys, time, socket, subprocess, pathlib
import pytest

def _find_free_port():
    import socket as s
    sock = s.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

@pytest.fixture(scope="session", autouse=True)
def live_server():
    # wipe local sqlite files so signup redirects (no duplicate user)
    for name in ("todo_app.db", "test_todo_app.db"):
        p = pathlib.Path(name)
        if p.exists():
            p.unlink()

    port = _find_free_port()
    env = os.environ.copy()
    env["APP_ENV"] = "test"
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", str(port)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    time.sleep(1.0)
    yield f"http://127.0.0.1:{port}"
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()

@pytest.fixture(scope="session")
def base_url(live_server):
    return live_server
