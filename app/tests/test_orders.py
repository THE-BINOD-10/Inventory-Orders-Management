from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

HEADERS = {"X-API-KEY": "mysecretkey"}

def test_order_insufficient_stock():
    response = client.post(
        "/orders",
        headers=HEADERS,
        json={
            "customer_name": "John",
            "items": [{"item_id": 1, "quantity": 999}]
        }
    )
    assert response.status_code == 400
