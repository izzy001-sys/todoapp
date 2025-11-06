from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas
from app.auth import verify_password, get_password_hash


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> models.User:
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate, owner_id: int) -> models.Todo:
    db_todo = models.Todo(**todo.model_dump(), owner_id=owner_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).filter(
        models.Todo.owner_id == owner_id
    ).offset(skip).limit(limit).all()


def get_todo_by_id(db: Session, todo_id: int, owner_id: int) -> models.Todo:
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.owner_id == owner_id
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoUpdate, owner_id: int) -> models.Todo:
    todo = get_todo_by_id(db, todo_id, owner_id)
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int, owner_id: int):
    todo = get_todo_by_id(db, todo_id, owner_id)
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

