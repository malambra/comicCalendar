import json
import datetime
import pytz
from app.models.events import Event

madrid_tz = pytz.timezone('Europe/Madrid')


async def load_events():
    with open("events.json", "r") as file:
        events_data = json.load(file)
        events = []
        for event_data in events_data:
            if 'update_date' not in event_data:
                event_data['update_date'] = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=madrid_tz).strftime("%Y-%m-%d %H:%M:%S")
            events.append(Event(**event_data))
        return events


async def save_events(events):
    with open("events.json", "w") as f:
        json.dump([event.dict() for event in events], f, ensure_ascii=False, indent=4)
