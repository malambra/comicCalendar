from fastapi import APIRouter, HTTPException, status, Depends
from app.utils.file_operations import load_events, save_events
from app.models.events import Event, EventMod
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.users import Token
from app.auth.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/v1")

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/events/{event_id}/", response_model=Event, dependencies=[Depends(get_current_user)], description="update values of event. Auth is required.", tags=["auth"])
async def update_event(event_id: int, event_update: EventMod):
    events = await load_events()
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
        await save_events(events)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al escribir en el archivo: {e}")

    return event

@router.post("/events/", response_model=Event, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)], description="Add new event. Auth is required.", tags=["auth"])
async def create_event(event: EventMod):
    events = await load_events()
    new_event_id = max(event.id for event in events) + 1 if events else 1
    event_data = event.dict()
    new_event = Event(id=new_event_id, **event_data)
    events.append(new_event)
    
    try:
        await save_events(events)
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")
        events.remove(new_event)
        raise HTTPException(status_code=500, detail=f"Error al escribir en el archivo: {e}")
    return new_event

@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)], description="Delete event by id. Auth is required.", tags=["auth"])
async def delete_event(event_id: int):
    events = await load_events()
    event_index = next((index for index, event in enumerate(events) if event.id == event_id), None)
    if event_index is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    del events[event_index]

    for index, event in enumerate(events):
        event.id = index + 1

    try:
        await save_events(events)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al escribir en el archivo: {e}")