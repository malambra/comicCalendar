from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime
from app.utils.file_operations import load_events, save_events
from app.models.events import Event, EventMod, EventListResponse
from app.auth.auth import authenticate 

router = APIRouter()

@router.get("/events/", response_model=EventListResponse, description="List events sorted by date.", tags=["events"])
async def read_events(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    events = await load_events()
    sorted_events = sorted(events, key=lambda event: event.start_date, reverse=True)
    total_events = len(events)
    return {"total": total_events, "events": sorted_events[offset : offset + limit]}

@router.get("/events/{event_id}", response_model=Event, description="Search event by id.", tags=["events"])
async def read_event(event_id: int):
    events = await load_events()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/events/search/", response_model=EventListResponse, description="Search events by date and/or province. If no params are provided, the current month is used.", tags=["events"])
async def search_events(date: str = None, province: str = None, limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    events = await load_events()
    filtered_events = events

    if not date and not province:
        date = datetime.now().strftime("%Y-%m")

    if date:
        filtered_events = [event for event in filtered_events if event.start_date.startswith(f"{date}") or event.end_date.startswith(f"{date}")]
    if province:
        filtered_events = [event for event in filtered_events if province.lower() in event.province.lower()]
    if not filtered_events:
        raise HTTPException(status_code=404, detail="No events found for the given criteria")
    
    sorted_events = sorted(filtered_events, key=lambda event: event.start_date, reverse=True)
    total_events = len(filtered_events)
    return {"total": total_events, "events": sorted_events[offset : offset + limit]}