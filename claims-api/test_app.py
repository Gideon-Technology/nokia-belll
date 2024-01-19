from fastapi.testclient import TestClient

from app import app as api_app


client = TestClient(api_app)


def test_read_main():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ready": True}
