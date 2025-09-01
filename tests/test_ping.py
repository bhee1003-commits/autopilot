from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ping():
    r = client.get("/api/ping")
    assert r.status_code == 200
    assert r.json() == {"pong": True}
