from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    organization = Column(String)
    email = Column(String, nullable=False)

class Chat(Base):
    __tablename__ = "chats"
    chat_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.user_id"))

class Message(Base):
    __tablename__ = "messages"
    message_id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "User" or "Assistant"
    timestamp = Column(DateTime)
    chat_id = Column(Integer, ForeignKey("chats.chat_id"))

DATABASE_URL = "sqlite:///med_qna.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
