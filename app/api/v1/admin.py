from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, Date, DateTime, Text, DECIMAL, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time, datetime
from decimal import Decimal
from passlib.context import CryptContext
import secrets
import string

from app.core.deps import get_db
from app.db.models import AdminQueue, ChatLog
from app.schemas.admin_queue import AdminQueueResponse, AdminQueueCreate, AdminQueueUpdate
from app.schemas.chat_log import ChatLogResponse, ChatLogCreate, ChatLogUpdate
# from app.core.security import pwd_ctx as pwd_context

router = APIRouter(prefix="/admin", tags=["admin"])


# Admin Queue CRUD Operations
@router.post("/admin_queue/", response_model=dict)
def create_admin_queue_item(item: AdminQueueCreate, db: Session = Depends(get_db)):
    db_item = AdminQueue(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Admin queue item created successfully", "queue_id": db_item.queue_id}

@router.get("/admin_queue/", response_model=List[AdminQueueResponse])
def read_admin_queue(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(AdminQueue).offset(skip).limit(limit).all()
    return items

@router.get("/admin_queue/{queue_id}", response_model=AdminQueueResponse)
def read_admin_queue_item(queue_id: int, db: Session = Depends(get_db)):
    item = db.query(AdminQueue).filter(AdminQueue.queue_id == queue_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Admin queue item not found")
    return item

@router.put("/admin_queue/{queue_id}", response_model=dict)
def update_admin_queue_item(queue_id: int, item: AdminQueueUpdate, db: Session = Depends(get_db)):
    db_item = db.query(AdminQueue).filter(AdminQueue.queue_id == queue_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Admin queue item not found")

    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    return {"message": "Admin queue item updated successfully"}

@router.delete("/admin_queue/{queue_id}", response_model=dict)
def delete_admin_queue_item(queue_id: int, db: Session = Depends(get_db)):
    db_item = db.query(AdminQueue).filter(AdminQueue.queue_id == queue_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Admin queue item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Admin queue item deleted successfully"}

@router.post("/chat_log/", response_model=dict)
def create_chat_log(item: ChatLogCreate, db: Session = Depends(get_db)):
    db_item = ChatLog(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Chat log created successfully", "chat_id": db_item.chat_id}

@router.get("/chat_log/", response_model=List[ChatLogResponse])
def read_chat_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(ChatLog).offset(skip).limit(limit).all()
    return items

@router.get("/chat_log/{chat_id}", response_model=ChatLogResponse)
def read_chat_log(chat_id: int, db: Session = Depends(get_db)):
    item = db.query(ChatLog).filter(ChatLog.chat_id == chat_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Chat log not found")
    return item

@router.get("/chat_log/user/{user_id}", response_model=List[ChatLogResponse])
def read_chat_logs_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(ChatLog).filter(ChatLog.user_id == user_id).offset(skip).limit(limit).all()
    return items

@router.put("/chat_log/{chat_id}", response_model=dict)
def update_chat_log(chat_id: int, item: ChatLogUpdate, db: Session = Depends(get_db)):
    db_item = db.query(ChatLog).filter(ChatLog.chat_id == chat_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Chat log not found")

    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    return {"message": "Chat log updated successfully"}

@router.delete("/chat_log/{chat_id}", response_model=dict)
def delete_chat_log(chat_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ChatLog).filter(ChatLog.chat_id == chat_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Chat log not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Chat log deleted successfully"}