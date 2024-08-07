from pydantic import BaseModel
from typing import List, Optional

class Event(BaseModel):
    id: int
    summary: str
    start_date: str
    end_date: str
    province: str
    address: str
    description: str

class EventMod(BaseModel):
    summary: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    province: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None

class EventListResponse(BaseModel):
    total: int
    events: List[Event]
