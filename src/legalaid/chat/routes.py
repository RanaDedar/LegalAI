from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response
from sqlalchemy.orm import Session
from legalaid.user.models import UserModel
from legalaid.chat import controller
from legalaid.chat.dtos import Querry_Schema
from legalaid.database.db import get_db

_CHAT_DIR = Path(__file__).resolve().parent

chat_router = APIRouter()


@chat_router.get("/chat")
async def serve_chat(request: Request):
    if request.session.get("uid") is None:
        return RedirectResponse(url="/user/auth", status_code=302)
    return FileResponse(_CHAT_DIR / "index.html")


@chat_router.post("/ask_agent", response_class=HTMLResponse)
async def ask_agent(
    request: Request,
    prompt: str = Form(...),
    db: Session = Depends(get_db),

):
    session_uid = request.session.get("uid")
    if session_uid is None:
        return Response(status_code=401, headers={"HX-Redirect": "/user/auth"})
    query = Querry_Schema(prompt=prompt, uid=int(session_uid))
    return await controller.ask_agent(query,db)
