import json
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def events_file_path():
    return os.path.join(os.path.dirname(__file__), 'events.json')

@pytest.fixture
def events(events_file_path):
    with open(events_file_path, 'r') as file:
        return json.load(file)

@pytest.fixture(autouse=True)
def mock_read_events(monkeypatch, events):
    async def mock_read_events(limit: int = 20, offset: int = 0):
        return {"total": len(events), "events": events}
    monkeypatch.setattr("app.routes.v1.event_routes.read_events", mock_read_events)

def test_read_events(events):
    response = client.get("/v1/events/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == len(events)
    assert len(data["events"]) == len(events)
    event_ids = [event["id"] for event in events]
    response_event_ids = [event["id"] for event in data["events"]]
    assert set(event_ids) == set(response_event_ids)  # Verifica que los eventos estén presentes

def test_read_event(events):
    event_id = 1
    response = client.get(f"/v1/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id
    assert data["summary"] == events[0]["summary"]
    assert data["start_date"] == events[0]["start_date"]
    assert data["end_date"] == events[0]["end_date"]
    assert data["address"] == events[0]["address"]
    assert data["description"] == events[0]["description"]
    assert data["type"] == events[0]["type"]
    assert data["city"] == events[0]["city"]
    assert data["province"] == events[0]["province"]
    assert data["community"] == events[0]["community"]

def test_read_event_not_found():
    event_id = 999
    response = client.get(f"/v1/events/{event_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Event not found"