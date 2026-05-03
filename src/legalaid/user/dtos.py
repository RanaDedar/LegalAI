import email
from pydantic import BaseModel
class User_Schema(BaseModel):
    name:str
    username:str
    email:str
    password:str
class Login_Schema(BaseModel):
    username:str
    password:str
