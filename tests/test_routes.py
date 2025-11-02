import pytest
from app import services, schemas


def test_signup(client):
    response = client.get("/signup")
    assert response.status_code == 200
    assert "Sign Up" in response.text


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "Login" in response.text


def test_signup_and_login_flow(client, db_session):
    # Sign up
    response = client.post(
        "/signup",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 303  # Redirect
    assert response.headers["location"] == "/"
    
    # Try to login
    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 303  # Redirect
    assert "access_token" in response.cookies


def test_create_todo_unauthorized(client):
    response = client.post(
        "/todos",
        json={"title": "Test Todo", "description": "Test"}
    )
    assert response.status_code == 401


def test_todo_crud(client, db_session):
    # Create user and get token
    user = services.create_user(
        db_session,
        schemas.UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    )
    
    from app.auth import create_access_token
    from datetime import timedelta
    token = create_access_token(data={"sub": user.username})
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create todo
    response = client.post(
        "/todos",
        json={"title": "Test Todo", "description": "Test Description"},
        headers=headers
    )
    assert response.status_code == 200
    todo_id = response.json()["id"]
    
    # Get todos
    response = client.get("/todos", headers=headers)
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Test Todo"
    
    # Get single todo
    response = client.get(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"
    
    # Update todo
    response = client.put(
        f"/todos/{todo_id}",
        json={"completed": True, "title": "Updated Todo"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["completed"] is True
    assert response.json()["title"] == "Updated Todo"
    
    # Delete todo
    response = client.delete(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 200
    
    # Verify deleted
    response = client.get("/todos", headers=headers)
    assert len(response.json()) == 0


def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 303
    assert response.headers["location"] == "/"

