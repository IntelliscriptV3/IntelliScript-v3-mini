from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdminQueueBase(BaseModel):
    chat_id: Optional[int] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    answered_by: Optional[int] = None

class AdminQueueCreate(AdminQueueBase):
    pass

class AdminQueueUpdate(BaseModel):
    chat_id: Optional[int] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    answered_by: Optional[int] = None

class AdminQueueResponse(AdminQueueBase):
    queue_id: int
    assigned_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AdminQueueInDB(AdminQueueResponse):
    pass






