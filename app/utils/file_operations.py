import json
from app.models.events import Event

def load_events():
    with open("events.json", "r") as file:
        events_data = json.load(file)
        return [Event(**event) for event in events_data]

def save_events(events):
    with open("events.json", "w") as f:
        json.dump([event.dict() for event in events], f, ensure_ascii=False, indent=4)