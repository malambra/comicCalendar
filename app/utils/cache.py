from typing import List
from datetime import datetime
from app.models.events import Event
from app.utils.file_operations import load_events

# Variable global para almacenar los eventos
cached_events: List[Event] = []
events_last_loaded: datetime = None

async def get_cached_events():
    global cached_events, events_last_loaded
    if not cached_events or (events_last_loaded and (datetime.now() - events_last_loaded).seconds > 3600):
        cached_events = await load_events()
        events_last_loaded = datetime.now()
    return cached_events

async def reload_cached_events():
    global cached_events, events_last_loaded
    cached_events = await load_events()
    events_last_loaded = datetime.now()