from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.utils.file_operations import load_events, save_events
from app.models.events import Event, EventMod
from app.auth.auth import authenticate 

router = APIRouter()

events = load_events()

@router.get("/events/", response_model=List[Event])
async def read_events():
    return events

@router.get("/events/by_date/", response_model=List[Event])
async def read_events_by_date(date: str):
    filtered_events = [event for event in events if event.start_date <= date <= event.end_date]
    if not filtered_events:
        raise HTTPException(status_code=404, detail="No events found for this date")
    return filtered_events

@router.get("/events/by_month/", response_model=List[Event])
async def read_events_by_month(year: int, month: int):
    month_str = f"{year}-{month:02d}"
    filtered_events = [event for event in events if month_str in event.start_date or month_str in event.end_date]
    if not filtered_events:
        raise HTTPException(status_code=404, detail="No events found for this month")
    return filtered_events

@router.get("/events/by_province/", response_model=List[Event])
async def read_events_by_province(province: str):
    filtered_events = [event for event in events if province.lower() in event.province.lower()]
    if not filtered_events:
        raise HTTPException(status_code=404, detail="No events found for this province")
    return filtered_events

@router.get("/events/by_province_and_month/", response_model=List[Event])
async def read_events_by_province_and_date(province: str, year: int, month: int):
    month_str = f"{year}-{month:02d}"
    filtered_events = [event for event in events if province.lower() in event.province.lower() and (month_str in event.start_date or month_str in event.end_date)]
    if not filtered_events:
        raise HTTPException(status_code=404, detail="No events found for this province and date")
    return filtered_events

@router.put("/events/{event_id}/", response_model=Event, dependencies=[Depends(authenticate)])
async def update_event(event_id: int, event_update: EventMod):
    event_index = None
    for index, event in enumerate(events):
        if event.id == event_id:
            event_index = index
            break

    if event_index is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event = events[event_index]
    if event_update.summary is not None:
        event.summary = event_update.summary
    if event_update.start_date is not None:
        event.start_date = event_update.start_date
    if event_update.end_date is not None:
        event.end_date = event_update.end_date
    if event_update.description is not None:
        event.description = event_update.description    
    if event_update.province is not None:
        event.province = event_update.province
    if event_update.address is not None:
        event.address = event_update.address
    events[event_index] = event

    try:
        save_events(events)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al escribir en el archivo: {e}")

    return event

@router.post("/events/", response_model=Event, status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate)])
async def create_event(event: EventMod):
    new_event_id = max(event.id for event in events) + 1 if events else 1
    event_data = event.dict()
    new_event = Event(id=new_event_id, **event_data)
    events.append(new_event)
    
    try:
        save_events(events)
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")
        events.remove(new_event)
        raise
    return new_event

@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(authenticate)])
async def delete_event(event_id: int):
    global events
    event_index = next((index for index, event in enumerate(events) if event.id == event_id), None)
    if event_index is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    del events[event_index]

    for index, event in enumerate(events):
        event.id = index + 1

    try:
        save_events(events)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al escribir en el archivo: {e}")