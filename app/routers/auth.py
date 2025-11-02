from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, services
from app.auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user_optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user_create = schemas.UserCreate(username=username, email=email, password=password)
        user = services.create_user(db, user_create)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response
    except HTTPException as e:
        current_user = await get_current_user_optional(request, db)
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": e.detail, "current_user": current_user}
        )


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, db: Session = Depends(get_db)):
    current_user = await get_current_user_optional(request, db)
    return templates.TemplateResponse(
        "signup.html",
        {"request": request, "current_user": current_user}
    )


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = services.authenticate_user(db, username, password)
    if not user:
        current_user = await get_current_user_optional(request, db)
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Incorrect username or password", "current_user": current_user}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    current_user = await get_current_user_optional(request, db)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "current_user": current_user}
    )


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response

