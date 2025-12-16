from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

HEADERS = {"X-API-KEY": "mysecretkey"}

def test_create_item():
    unique_name = f"Test Item {uuid.uuid4()}"
    response = client.post(
        "/items",
        headers=HEADERS,
        json={
            "name": unique_name,
            "price": 100,
            "quantity": 10
        }
    )
    assert response.status_code == 200
