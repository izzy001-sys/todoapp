import pytest
from app import services, schemas, models
from sqlalchemy.orm import Session


def test_create_user(db_session: Session):
    user_data = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    user = services.create_user(db_session, user_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.id is not None


def test_create_user_duplicate_username(db_session: Session):
    user_data = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    services.create_user(db_session, user_data)
    
    duplicate_user = schemas.UserCreate(
        username="testuser",
        email="test2@example.com",
        password="testpass123"
    )
    with pytest.raises(Exception):
        services.create_user(db_session, duplicate_user)


def test_authenticate_user(db_session: Session):
    user_data = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    services.create_user(db_session, user_data)
    
    authenticated = services.authenticate_user(db_session, "testuser", "testpass123")
    assert authenticated is not None
    assert authenticated.username == "testuser"
    
    wrong_password = services.authenticate_user(db_session, "testuser", "wrongpass")
    assert wrong_password is None
    
    wrong_username = services.authenticate_user(db_session, "wronguser", "testpass123")
    assert wrong_username is None


def test_create_todo(db_session: Session):
    user_data = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    user = services.create_user(db_session, user_data)
    
    todo_data = schemas.TodoCreate(
        title="Test Todo",
        description="Test Description"
    )
    todo = services.create_todo(db_session, todo_data, user.id)
    assert todo.title == "Test Todo"
    assert todo.description == "Test Description"
    assert todo.owner_id == user.id
    assert todo.completed is False


def test_get_todos(db_session: Session):
    user_data = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    user = services.create_user(db_session, user_data)
    
    todo1 = services.create_todo(db_session, schemas.TodoCreate(title="Todo 1"), user.id)
    todo2 = services.create_todo(db_session, schemas.TodoCreate(title="Todo 2"), user.id)
    
    todos = services.get_todos(db_session, user.id)
    assert len(todos) == 2
    assert todos[0].id == todo1.id or todos[1].id == todo1.id


def test_update_todo(db_session: Session):
    user_data = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    user = services.create_user(db_session, user_data)
    
    todo = services.create_todo(db_session, schemas.TodoCreate(title="Test Todo"), user.id)
    
    update_data = schemas.TodoUpdate(completed=True, title="Updated Todo")
    updated_todo = services.update_todo(db_session, todo.id, update_data, user.id)
    
    assert updated_todo.completed is True
    assert updated_todo.title == "Updated Todo"


def test_delete_todo(db_session: Session):
    user_data = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    user = services.create_user(db_session, user_data)
    
    todo = services.create_todo(db_session, schemas.TodoCreate(title="Test Todo"), user.id)
    
    result = services.delete_todo(db_session, todo.id, user.id)
    assert result["message"] == "Todo deleted successfully"
    
    todos = services.get_todos(db_session, user.id)
    assert len(todos) == 0

