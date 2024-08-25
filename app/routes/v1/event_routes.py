from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.models.events import Event, EventListResponse
from app.utils.cache import get_cached_events  # Importar desde cache.py

router = APIRouter(prefix="/v1")


@router.get(
    "/events/",
    response_model=EventListResponse,
    description="List events sorted by date.",
    tags=["events"],
)
async def read_events(
    limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)
):
    events = await get_cached_events()
    sorted_events = sorted(events, key=lambda event: event.start_date, reverse=True)
    total_events = len(events)
    return {"total": total_events, "events": sorted_events[offset : offset + limit]}


@router.get(
    "/events/{event_id}",
    response_model=Event,
    description="Search event by id.",
    tags=["events"],
)
async def read_event(event_id: int):
    events = await get_cached_events()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get(
    "/events/search/",
    response_model=EventListResponse,
    description="Search events by date and/or province. If no params are provided, the current month is used.",
    tags=["events"],
)
async def search_events(
    province: str = None,
    community: str = None,
    city: str = None,
    type: str = None,
    start_date: str = Query(None, description="Format: YYYY-MM-DD"),
    end_date: str = Query(None, description="Format: YYYY-MM-DD"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    events = await get_cached_events()
    filtered_events = events

    if start_date or end_date:
        if not start_date or not end_date:
            # Calcular las fechas mínimas y máximas de los eventos disponibles en caso de no recibir start_date o end_date
            event_dates = [
                datetime.fromisoformat(event.start_date).date() for event in events
            ] + [datetime.fromisoformat(event.end_date).date() for event in events]
            min_date = min(event_dates)
            max_date = max(event_dates)

        if not start_date:
            start_date_dt = min_date
            print(start_date_dt)
        else:
            start_date_dt = datetime.fromisoformat(start_date).date()
            print(start_date_dt)

        if not end_date:
            end_date_dt = max_date
            print(end_date_dt)
        else:
            end_date_dt = datetime.fromisoformat(end_date).date()
            print(end_date_dt)

        filtered_events = [
            event
            for event in filtered_events
            if start_date_dt
            <= datetime.fromisoformat(event.start_date).date()
            <= end_date_dt
            or start_date_dt
            <= datetime.fromisoformat(event.end_date).date()
            <= end_date_dt
        ]
    if province:
        filtered_events = [
            event
            for event in filtered_events
            if province.lower() in event.province.lower()
        ]
    if community:
        filtered_events = [
            event
            for event in filtered_events
            if community.lower() in event.community.lower()
        ]
    if city:
        filtered_events = [
            event for event in filtered_events if city.lower() in event.city.lower()
        ]
    if type:
        filtered_events = [
            event for event in filtered_events if type.lower() in event.type.lower()
        ]
    if not filtered_events:
        raise HTTPException(
            status_code=404, detail="No events found for the given criteria"
        )

    sorted_events = sorted(
        filtered_events, key=lambda event: event.start_date, reverse=True
    )
    total_events = len(filtered_events)
    return {"total": total_events, "events": sorted_events[offset : offset + limit]}
