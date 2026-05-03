from pathlib import Path
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from legalaid.database.db import get_db
from legalaid.user import controller
from legalaid.user.dtos import Login_Schema, User_Schema

_USER_DIR = Path(__file__).resolve().parent
user_routes = APIRouter()
@user_routes.get("/auth", response_class=HTMLResponse)
async def get_auth_page(request: Request):
    if request.session.get("uid") is not None:
        return RedirectResponse(url="/chat", status_code=302)
    return FileResponse(_USER_DIR / "auth.html")
@user_routes.get("/register", response_class=HTMLResponse)
async def get_register_form():
    return controller.get_register_fragment()
@user_routes.get("/login", response_class=HTMLResponse)
async def get_login_form():
    return controller.get_login_fragment()
@user_routes.post("/register")
async def register(
    name: str = Form(...), 
    username: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    body = User_Schema(name=name, username=username, email=email, password=password)
    return controller.register_user(body, db)
@user_routes.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    body = Login_Schema(username=username, password=password)
    return controller.login(body, db, request)
