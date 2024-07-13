from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./events.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class EventType(PyEnum):
    CLIENT_CREATED = "CLIENT_CREATED"
    BALANCE_UPDATED = "BALANCE_UPDATED"
    CLIENT_DELETED = "CLIENT_DELETED"
    CLIENT_RESTORED = "CLIENT_RESTORED"
    
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(Enum(EventType), index=True)
    data = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)