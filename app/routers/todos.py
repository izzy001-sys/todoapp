from typing import List
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, services, models
from app.auth import get_current_user, get_current_user_optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    current_user = await get_current_user_optional(request, db)
    todos = []
    if current_user:
        todos = services.get_todos(db, owner_id=current_user.id)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "current_user": current_user, "todos": todos}
    )


@router.post("/todos", response_model=schemas.TodoResponse)
async def create_todo(
    todo: schemas.TodoCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return services.create_todo(db, todo, current_user.id)


@router.get("/todos", response_model=List[schemas.TodoResponse])
async def read_todos(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todos = services.get_todos(db, owner_id=current_user.id, skip=skip, limit=limit)
    return todos


@router.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
async def read_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return services.get_todo_by_id(db, todo_id, current_user.id)


@router.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: schemas.TodoUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return services.update_todo(db, todo_id, todo_update, current_user.id)


@router.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return services.delete_todo(db, todo_id, current_user.id)

