from fastapi.testclient import TestClient
from week1.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert "model" in body