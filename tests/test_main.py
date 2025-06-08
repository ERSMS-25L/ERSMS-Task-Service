from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

def test_create_task():
    response = client.post("/tasks", json={
        "title": "Write tests",
        "description": "Test endpoint for task creation"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Write tests"

def test_list_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
