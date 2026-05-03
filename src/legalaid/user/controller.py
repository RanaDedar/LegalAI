from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from  legalaid.user.dtos import User_Schema,Login_Schema
from sqlalchemy.orm import Session
from legalaid.user.models import UserModel
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
def get_passwordhash(password):
    return password_hash.hash(password)
def verify_password(plain_password,hash_password):
    return password_hash.verify(plain_password,hash_password)
def get_register_fragment():
    return HTMLResponse(content="""
        <h1>Register</h1>
        <form hx-post="/user/register" hx-target="#auth-container">
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit" class="btn">Create Account</button>
        </form>
        <span class="toggle-link" hx-get="/user/login" hx-target="#auth-container">
            Already have an account? Log in
        </span>
    """)
_LOGIN_FRAGMENT_HTML = """
        <h1>Log In</h1>
        <form hx-post="/user/login" hx-target="#auth-container">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit" class="btn">Enter Portal</button>
        </form>
        <span class="toggle-link" hx-get="/user/register" hx-target="#auth-container">
            New here? Register your self!
        </span>
    """
def get_login_fragment():
    return HTMLResponse(content=_LOGIN_FRAGMENT_HTML)
def register_user(body:User_Schema,db:Session):
    username=db.query(UserModel).filter(UserModel.username==body.username).first()
    if username:
        raise HTTPException(401,detail="username already exists")
    useremail=db.query(UserModel).filter(UserModel.email==body.email).first()
    if useremail:
        raise HTTPException (401,detail="user email already exist")
    hash_password=get_passwordhash(body.password)
    new_user=UserModel(
        name=body.name,
        username=body.username,
        email=body.email,
        hash_password=hash_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return HTMLResponse(
        content="<p style='color: #c5a059;'>Account created! Please log in.</p>" + _LOGIN_FRAGMENT_HTML
    )
def login(body: Login_Schema, db: Session, request: Request):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(401, detail="user not found")
    if not verify_password(body.password, user.hash_password):
        raise HTTPException(401, detail="Wrong password entered")
    request.session["uid"] = user.id
    request.session["username"] = user.username
    return Response(status_code=200, headers={"HX-Redirect": "/chat"})
