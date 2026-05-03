from sqlalchemy import Column, DateTime,Integer,String,Boolean,ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from legalaid.database.db import Base


class ChatSession(Base):
    __tablename__="chat_sessions"
    id=Column(Integer,primary_key=True)
    uid=Column(Integer,ForeignKey("User_Table.id"))
    timestamp=Column(DateTime,default=datetime.now)
    messages = relationship("ChatMessage", back_populates="session")
class ChatMessage(Base):
    __tablename__="chat_messages"
    id=Column(Integer,primary_key=True)
    sid=Column(Integer,ForeignKey("chat_sessions.id"))
    role=Column(String)
    content=Column(Text)
    session=relationship("ChatSession",back_populates="messages")