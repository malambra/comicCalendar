from fastapi import APIRouter, HTTPException, status, Depends
from app.utils.file_operations import load_events, save_events
from app.utils.validate_data import validate_province_and_community
from app.models.events import Event, EventMod
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from app.models.users import Token, TokenData
from app.auth.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.utils.cache import reload_cached_events  # Importar desde cache.py

router = APIRouter(prefix="/v1")

@router.post("/token", description="Create new token", response_model=Token)
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


@router.get("/token/validate", description="Validate if the token is still valid.")
async def validate_token(token_data: TokenData = Depends(verify_token)):
    expiration_time = datetime.utcfromtimestamp(token_data.expiration)
    formatted_expiration = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    return {
        "message": "Token is valid",
        "username": token_data.username,
        "expires_at": formatted_expiration,
    }


@router.put(
    "/events/{event_id}/",
    response_model=Event,
    dependencies=[Depends(get_current_user)],
    description="Update values of event. Auth is required.",
    tags=["auth"],
)
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

    # Validar la provincia y la comunidad (si se actualizan)
    if event_update.province is not None and event_update.community is not None:
        if not validate_province_and_community(
            event_update.province, event_update.community
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La provincia no pertenece a la comunidad autónoma proporcionada.",
            )

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
    if event_update.community is not None:
        event.community = event_update.community
    if event_update.city is not None:
        event.city = event_update.city
    if event_update.type is not None:
        event.type = event_update.type
    if event_update.address is not None:
        event.address = event_update.address
    events[event_index] = event
    try:
        await save_events(events)
        await reload_cached_events()  # Recargar los eventos en caché
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al escribir en el archivo: {e}"
        )
    return event


@router.post(
    "/events/",
    response_model=Event,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
    description="Add new event. Auth is required.",
    tags=["auth"],
)
async def create_event(event: EventMod):
    # Validar la provincia y la comunidad
    if not validate_province_and_community(event.province, event.community):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La provincia no pertenece a la comunidad autónoma proporcionada.",
        )
    events = await load_events()
    new_event_id = max((event.id for event in events), default=0) + 1

    event_data = event.dict()
    new_event = Event(id=new_event_id, **event_data)
    events.append(new_event)
    try:
        await save_events(events)
        await reload_cached_events()  # Recargar los eventos en caché
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")
        events.remove(new_event)
        raise HTTPException(
            status_code=500, detail=f"Error al escribir en el archivo: {e}"
        )
    return new_event


@router.delete(
    "/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
    description="Delete event by id. Auth is required.",
    tags=["auth"],
)
async def delete_event(event_id: int):
    events = await load_events()
    event_index = next(
        (index for index, event in enumerate(events) if event.id == event_id), None
    )

    if event_index is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    del events[event_index]

    try:
        await save_events(events)
        await reload_cached_events()  # Recargar los eventos en caché
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al escribir en el archivo: {e}"
        )
    return {"message": "Evento eliminado con éxito"}