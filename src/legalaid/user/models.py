from sqlalchemy import Column,String,Integer,Boolean
from legalaid.database.db import Base
class UserModel(Base):
    __tablename__="User_Table"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    username=Column(String,nullable=False)
    email=Column(String)
    hash_password=Column(String,nullable=False)