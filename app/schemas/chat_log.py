from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ChatLogBase(BaseModel):
    user_id: int
    question: str
    answer: str
    confidence_score: Optional[Decimal] = Field(None, ge=0, le=9.999, decimal_places=3)
    status: Optional[str] = None

class ChatLogCreate(ChatLogBase):
    pass

class ChatLogUpdate(BaseModel):
    user_id: Optional[int] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    confidence_score: Optional[Decimal] = Field(None, ge=0, le=9.999, decimal_places=3)
    status: Optional[str] = None

class ChatLogResponse(ChatLogBase):
    chat_id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None
        }

class ChatLogInDB(ChatLogResponse):
    pass