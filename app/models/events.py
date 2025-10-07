from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Event(BaseModel):
    id: int
    summary: str
    start_date: str
    end_date: str
    create_date: str
    update_date: str
    province: str
    community: str
    city: str
    type: str
    address: str
    description: str


class EventMod(BaseModel):
    summary: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    create_date: Optional[str] = None
    update_date: Optional[str] = None
    province: Optional[str] = None
    community: Optional[str] = None
    city: Optional[str] = None
    type: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None


class EventListResponse(BaseModel):
    total: int
    last_updated: datetime
    events: List[Event]
