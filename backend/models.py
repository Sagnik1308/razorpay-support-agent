from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class ChatRequest(BaseModel):
    session_id: str
    message: str
    user_name: Optional[str] = None

class Source(BaseModel):
    url: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
    suggested_quick_replies: List[str] = []
    escalatable: bool = True

class FeedbackRequest(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    question: str = Field(min_length=3)
    session_id: Optional[str] = None
