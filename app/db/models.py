from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Time, Boolean, DECIMAL,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from .session import Base

# ---------- Existing tables (as in your seed.py) ----------


class ChatLog(Base):
    __tablename__ = 'chat_logs'
    chat_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    question = Column(Text)
    answer = Column(Text)
    confidence_score = Column(DECIMAL(4,3))
    status = Column(String)
    created_at = Column(DateTime)


class AdminQueue(Base):
    __tablename__ = 'admin_queue'
    queue_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    question = Column(Text)
    answer = Column(Text)
    answered_by = Column(Integer)
    assigned_at = Column(DateTime)

